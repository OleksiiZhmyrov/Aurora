from SOAPpy import Types

from SOAPpy.WSDL import Proxy

from logger import LOGGER

from settings import JIRA_SETTINGS, CUSTOM_FIELDS, STATUS_CODES, BACKLOG_DEFECTS_QUERY


class JiraSettings(object):
    def __init__(self):
        self.login = JIRA_SETTINGS['login']
        self.password = JIRA_SETTINGS['password']
        self.project = JIRA_SETTINGS['project']
        self.uri = JIRA_SETTINGS['uri']
        self.browse = JIRA_SETTINGS['browse']


class JiraIssue(object):
    def __init__(self):
        self.key = None
        self.raw = None
        self.reporter = None
        self.summary = None
        self.status = None
        self.dc_status = ''
        self.custom_fields = {}

    def parse_args(self, key, reporter, summary, status, dc_status, custom_fields):
        self.key = key
        self.reporter = reporter
        self.summary = summary
        self.status = status
        self.dc_status = dc_status
        self.custom_fields = custom_fields

    def parse_raw(self, raw):
        self.raw = raw
        self.key = self.raw.key
        self.reporter = self.raw.reporter.replace('_', ' ')
        self.summary = self.raw.summary.encode('ascii', 'ignore')
        self.status = self.__get_status()
        self.custom_fields = self.__get_custom_fields()

    def get_custom_field(self, field_key):
        result = ''
        try:
            result = self.custom_fields[field_key]
        except KeyError:
            LOGGER.warn('Issue %s does not have value for field %s' % (self.key, field_key))
        return result

    def __get_status(self):
        status = None
        code = self.raw.status
        if code is not None:
            if code in STATUS_CODES.keys():
                status = STATUS_CODES[code]
            else:
                status = 'unknown code %s' % code
        return status

    def __get_custom_fields(self):
        result = dict()
        for node in self.raw:
            if type(node) == Types.typedArrayType:
                for item in node:
                    try:
                        field_id = item.customfieldId
                        if field_id in CUSTOM_FIELDS.keys():
                            result[CUSTOM_FIELDS[field_id]] = item.values[0].replace('_', ' ')
                    except AttributeError:
                        continue
        return result

    def __str__(self):
        line = '%s %s' % (self.key, unicode(self.summary))
        return line.encode('ascii', 'ignore')


class JiraInstance(object):
    def __init__(self):
        self.settings = JiraSettings()
        self.proxy = Proxy(self.settings.uri)

    def get_token(self):
        LOGGER.info('Logging in to Jira as %s' % self.settings.login)
        token = self.proxy.login(self.settings.login, self.settings.password)
        return token

    def get_backlog_defects_count(self):
        request = BACKLOG_DEFECTS_QUERY
        response = self.proxy.getIssuesFromJqlSearch(self.get_token(), request, Types.intType(1000))
        return len(response)

    def get_issues(self, issues, limit=300):
        result = []
        keys = ','.join(issues)
        request = 'project=%s AND key in (%s)' % (self.settings.project, keys)
        LOGGER.debug(request)
        response = self.proxy.getIssuesFromJqlSearch(self.get_token(), request, Types.intType(limit))

        for item in response:
            issue = JiraIssue()
            issue.parse_raw(item)
            result.append(issue)
        return result
