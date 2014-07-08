from confluence import ConfluenceInstance
from jira import JiraInstance
from database import DatabaseWrapper


class Aurora(object):
    def __init__(self):
        self.__kb = ConfluenceInstance()
        self.__jira = JiraInstance()
        self.__db = DatabaseWrapper()

    def update(self):
        page = self.__kb.get_page()
        initial_page_hash = page.get_hash()
        keys = page.get_story_keys()
        self.__db.clear()

        self.__db.lock_database()
        for issue in self.__jira.get_issues(keys):
            self.__db.store_issue(issue)
            page.update_row(issue)

        self.__db.update_issue_status(page.get_stories_data())
        self.__db.update_defect_count(self.__jira.get_backlog_defects_count())

        updated_page_hash = page.get_hash()

        if updated_page_hash != initial_page_hash:
            self.__kb.save_page(page)

        self.__db.unlock_database()

if __name__ == '__main__':
    aurora = Aurora()
    aurora.update()

