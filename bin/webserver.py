from argparse import ArgumentParser

from flask import Flask, render_template
from database import DatabaseWrapper
from stats import Stats
from jira import JiraSettings
from settings import SPRINT_NAME
from time import strftime

app = Flask(__name__)
app.debug = True


@app.route('/')
def home_page():
    return 'Homepage!'


@app.route('/progress')
def progress_page():
    db = DatabaseWrapper()
    if db.is_locked():
        return render_template('out_of_order.html')
    else:
        stats = Stats(db.get_dc_issues())
        defects = db.get_defect_count()
        datetime = db.get_unlock_datetime().strftime("%Y-%m-%d %H:%M:%S %z")
        return render_template('progress.html', statistics=stats.get_result(), sprint=SPRINT_NAME, defects=defects, datetime=datetime)


@app.route('/outdated')
def outdated_page():
    db = DatabaseWrapper()
    if db.is_locked():
        return render_template('out_of_order.html')
    else:
        browse_url = JiraSettings().browse
        return render_template('outdated.html', issues=db.get_outdated_issues(), browse_url=browse_url, sprint=SPRINT_NAME)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-H", "--host", nargs='?', default="localhost", help="Hostname or IP address to listen")
    parser.add_argument("-P", "--port", nargs='?', default=8080, help="Port to listen")
    args = parser.parse_args()
    app.run(str(args.host), int(args.port))