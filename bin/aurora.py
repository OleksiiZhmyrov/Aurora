from confluence import ConfluenceInstance
from jira import JiraInstance
from database import DatabaseWrapper


kb = ConfluenceInstance()
jira = JiraInstance()
db = DatabaseWrapper()

page = kb.get_page()
keys = page.get_story_keys()

db.clear()

for issue in jira.get_issues(keys):
    db.store_issue(issue)
    page.update_row(issue)

#kb.save_page(page)
