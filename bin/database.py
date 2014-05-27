from json import dumps as to_json
from json import loads as from_json

from peewee import Model, CharField, SqliteDatabase, TextField, DeleteQuery, DoesNotExist

from jira import JiraIssue

from logger import LOGGER
from settings import DATABASE_FILENAME


database = SqliteDatabase(DATABASE_FILENAME)
database.connect()


class BaseModel(Model):
    class Meta:
        database = database


class DbJiraIssues(BaseModel):
    key = CharField()
    summary = CharField()
    status = CharField()
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
    def get_all_issues():
        result = []
        for db_record in DbJiraIssues.select():
            result.append(DatabaseWrapper.__record_to_issue(db_record))
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
            custom_fields=from_json(db_record.custom_fields),
        )
        return issue
