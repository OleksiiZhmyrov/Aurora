# Copy this file as settings.py and fill in parameters

CONFLUENCE_SETTINGS = {
    'login': '',
    'password': '',
    'namespace': '',
    'uri': 'https://hostname:port/rpc/xmlrpc',
    'pagename': '',
}

JIRA_SETTINGS = {
    'login': '',
    'password': '',
    'project': '',
    'uri': 'https://hostname:port/jira/rpc/soap/jirasoapservice-v2?WSDL',
    'browse': 'https://hostname:port/jira/browse/',
}

CUSTOM_FIELDS = {
    '1': 'points',
    '2': 'tester',
    '3': 'is_dc',
    '4': 'team',
    '5': 'est_date',
    '6': 'onshore_ba',
}

STATUS_CODES = {
    '1': 'in progress',
    '2': 'defined',
    '3': 'completed',
    '4': 'accepted',
    '5': 'in development',
    '6': 'in testing',
}

COLOURS = {
    'in progress': 'rgb(255,128,0)',
    'completed': 'rgb(0,0,255)',
    'accepted': 'rgb(153,204,0)',
    'in development': 'rgb(0,0,0)',
    'in testing': 'rgb(0,0,0)',
    'default': 'rgb(0,0,0)',
}

DATABASE_FILENAME = '../db.sqlite3'
SPRINT_NAME = ''