from argparse import ArgumentParser

from flask import Flask, render_template
from database import DatabaseWrapper
from stats import Stats
from jira import JiraSettings

app = Flask(__name__)
app.debug = True


@app.route('/')
def home_page():
    return 'Homepage!'


@app.route('/progress')
def progress_page():
    stats = Stats(DatabaseWrapper.get_all_issues())
    return render_template('progress.html', statistics=stats.get_result())


@app.route('/outdated')
def outdated_page():
    browse_url = JiraSettings().browse
    return render_template('outdated.html', issues=DatabaseWrapper.get_outdated_issues(), browse_url=browse_url)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-H", "--host", nargs='?', default="localhost", help="Hostname or IP address to listen")
    parser.add_argument("-P", "--port", nargs='?', default=8080, help="Port to listen")
    args = parser.parse_args()
    app.run(str(args.host), int(args.port))