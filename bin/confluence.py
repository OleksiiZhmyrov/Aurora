from xmlrpclib import Server

from bs4 import BeautifulSoup

from logger import LOGGER

from util import fail, format_date
from settings import COLOURS, CONFLUENCE_SETTINGS


class ConfluenceSettings(object):
    def __init__(self):
        self.login = CONFLUENCE_SETTINGS['login']
        self.password = CONFLUENCE_SETTINGS['password']
        self.namespace = CONFLUENCE_SETTINGS['namespace']
        self.uri = CONFLUENCE_SETTINGS['uri']
        self.pagename = CONFLUENCE_SETTINGS['pagename']


class ConfluencePage(object):
    def __init__(self, data):
        self.data = data
        self.soup = BeautifulSoup(self.get_content())

    def get_content(self):
        return self.data.get('content')

    def set_content(self, content):
        self.data.update({'content': str(content)})

    def get_story_keys(self):
        result = []
        for row in self.soup.findAll('tr')[1:]:
            if len(row.findAll('td')) != 12:
                fail('column count is incorrect')
            cols = row.findAll('td')
            if cols[2].find('a') is None:
                fail('story key is not a hyperlink')
            else:
                result.append(str(cols[2].find("a").text))
        LOGGER.info('Table contains %s stories' % len(result))
        return result

    def update_row(self, jira_issue):
        for row in self.soup.findAll('tr')[1:]:
            key = row.findAll('td')[2].text
            if key == jira_issue.key:
                ConfluencePage.__update_cell(row, 3, None, jira_issue.summary)
                ConfluencePage.__update_cell(row, 4, ConfluencePage.__get_colour(jira_issue.status), jira_issue.status)
                ConfluencePage.__update_cell(row, 5, None, jira_issue.get_custom_field('is_dc'))
                ConfluencePage.__update_cell(row, 7, None, jira_issue.reporter)
                ConfluencePage.__update_cell(row, 8, None, jira_issue.get_custom_field('onshore_ba'))
                ConfluencePage.__update_cell(row, 9, None, format_date(jira_issue.get_custom_field('est_date')))

        self.set_content(self.soup.find('table'))

    @staticmethod
    def __update_cell(row, index, colour, value):
        if colour is not None:
            tag = BeautifulSoup(
                '<td><span style="color: {colour};">{value}</span></td>'.format(colour=colour, value=value)).td
        else:
            tag = BeautifulSoup('<td>{value}</td>'.format(value=value)).td
        row.findAll('td')[index].replaceWith(tag)

    @staticmethod
    def __get_colour(field_value):
        if field_value in COLOURS.keys():
            return COLOURS[field_value]
        else:
            return COLOURS['default']

    def __str__(self):
        return str(self.get_content())


class ConfluenceInstance(object):
    def __init__(self):
        self.settings = ConfluenceSettings()
        self.server = Server(self.settings.uri).confluence2
        self.page = None

    def get_token(self):
        LOGGER.info('Logging in to Confluence as %s' % self.settings.login)
        token = self.server.login(self.settings.login, self.settings.password)
        return token

    def get_page(self):
        if self.page is None:
            LOGGER.info('Fetching page contents from Confluence')
            data = self.server.getPage(
                self.get_token(),
                self.settings.namespace,
                self.settings.pagename
            )
            self.page = ConfluencePage(data)
        return self.page

    def save_page(self, page):
        self.server.storePage(self.get_token(), page.data)
