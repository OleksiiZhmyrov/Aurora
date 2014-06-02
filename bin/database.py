from json import dumps as to_json
from json import loads as from_json
from datetime import datetime

from peewee import Model, CharField, SqliteDatabase, TextField, DeleteQuery, DoesNotExist

from jira import JiraIssue
from logger import LOGGER
from settings import DATABASE_FILENAME


database = SqliteDatabase(DATABASE_FILENAME, threadlocals=True)
database.connect()


class BaseModel(Model):
    class Meta:
        database = database


class DbJiraIssues(BaseModel):
    key = CharField()
    summary = CharField()
    status = CharField()
    dc_status = CharField(null=True)
    reporter = CharField(null=True)
    custom_fields = TextField(null=True)


class DatabaseWrapper:
    def __init__(self):
        if not DbJiraIssues.table_exists():
            DbJiraIssues.create_table()

    @staticmethod
    def store_issue(issue):
        db_record = DbJiraIssues(
            key=issue.key,
            summary=issue.summary,
            status=issue.status,
            reporter=issue.reporter,
            custom_fields=to_json(issue.custom_fields),
        )
        db_record.save()

    @staticmethod
    def update_issue_status(status_list):
        for item in status_list:
            status = item['status'].upper()
            key = item['key']
            update_query = DbJiraIssues.update(dc_status=status).where(DbJiraIssues.key == key)
            update_query.execute()
            LOGGER.debug(update_query)

    @staticmethod
    def get_all_issues():
        result = []
        for db_record in DbJiraIssues.select():
            result.append(DatabaseWrapper.__record_to_issue(db_record))
        return result

    @staticmethod
    def get_dc_issues():
        return [issue for issue in DatabaseWrapper.get_all_issues() if issue.get_custom_field('is_dc') == 'Yes']

    @staticmethod
    def get_outdated_issues():
        result = []
        now = datetime.now().date()
        for issue in DatabaseWrapper.get_all_issues():
            if issue.get_custom_field('est_date') != '':
                try:
                    est_date = datetime.strptime(issue.get_custom_field('est_date'), '%d/%b/%y').date()
                    if est_date <= now and issue.status in ('in progress', 'defined'):
                        issue.est_date = est_date
                        issue.team = issue.get_custom_field('team')
                        issue.points = issue.get_custom_field('points')
                        if est_date < now:
                            issue.outdated = True
                        result.append(issue)
                except ValueError:
                    LOGGER.debug(
                        'Unexpected date format for issue %s: %s' % (issue.key, issue.get_custom_field('est_date')))
        result.sort(key=lambda issue: issue.est_date)
        return result

    @staticmethod
    def get_issue(key):
        try:
            db_record = DbJiraIssues.get(DbJiraIssues.key == key)
            return DatabaseWrapper.__record_to_issue(db_record)
        except DoesNotExist:
            LOGGER.warn('Issue %s does not exist in database' % key)

    @staticmethod
    def clear():
        query = DeleteQuery(DbJiraIssues)
        query.execute()

    @staticmethod
    def __record_to_issue(db_record):
        issue = JiraIssue()
        issue.parse_args(
            key=db_record.key,
            reporter=db_record.reporter,
            summary=db_record.summary,
            status=db_record.status,
            dc_status=db_record.dc_status,
            custom_fields=from_json(db_record.custom_fields),
        )
        return issue
