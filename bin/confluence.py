from xmlrpclib import Server

from bs4 import BeautifulSoup
from time import gmtime, strftime
from logger import LOGGER

from util import fail, format_date
from database import DatabaseWrapper
from stats import Stats
from settings import COLOURS, CONFLUENCE_SETTINGS
from confluence_templ import update_message, structured_macro, paragraph


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
        try:
            return self.data.get('content')
        except KeyError:
            LOGGER.error('Confluence page does not have content')
            return None

    def set_content(self, content):
        self.data.update({'content': str(content)})

    def get_story_keys(self):
        return [item['key'] for item in self.get_stories_data()]

    def get_stories_data(self):
        result = []
        for row in self.soup.findAll('tr')[1:]:
            if len(row.findAll('td')) != 12:
                fail('column count is incorrect')
            cols = row.findAll('td')
            if cols[2].find('a') is None:
                fail('story key is not a hyperlink')
            else:
                result.append({
                    'key': str(cols[2].find("a").text),
                    'status': str(cols[6].text.encode('ascii', 'ignore'))
                })
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

                est_date = jira_issue.get_custom_field('est_date')
                if est_date != '':
                    est_date = format_date(est_date)
                ConfluencePage.__update_cell(row, 9, None, est_date)

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
        self.db = DatabaseWrapper()
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
        page = self.__attach_statistics(page)
        self.server.storePage(self.get_token(), page.data)

    def __attach_statistics(self, page):
        stats = Stats(self.db.get_all_issues()).get_result()
        content = page.data['content']
        message = paragraph(update_message(self.settings.login, strftime("%Y-%m-%d %H:%M:%S %z", gmtime())))
        stat_info = paragraph(
            structured_macro('Grey', '%s total' % stats['total']['count']) +
            structured_macro('Blue', '%s ready' % stats['ready']['count']) +
            structured_macro('Green', '%s pass' % stats['passed']['count']) +
            structured_macro('Red', '%s fail' % stats['failed']['count'])
        )
        content = message + stat_info + content
        page.data.update({'content': str(content)})
        return page