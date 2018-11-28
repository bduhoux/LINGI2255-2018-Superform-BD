import os
from superform.models import db, Publishing
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.base import STATE_RUNNING
from superform.utils import login_required
import json, time
from flask import Blueprint, url_for, redirect, request, Flask

archival_page = Blueprint('archival', __name__)

scheduler = BackgroundScheduler()

# By default, the archival_job is scheduled at 00:01 :
HOUR_DEFAULT = 0
MINUT_DEFAULT = 1

FILE_PATH = os.path.dirname(os.path.abspath(__file__)) + '/config.json'
ARCHIVAL_KEY = "ARCHIVAL_JOB"
HOUR_KEY = "hour"
MINUT_KEY = "minut"
SQL_URI_KEY = "SQLALCHEMY_DATABASE_URI"
SQL_TRACK_KEY = "SQLALCHEMY_TRACK_MODIFICATIONS"

def get_archival_config():
    """
    :return: a JSON as {<HOUR_KEY>: ..., <MINUT_KEY>: ... }
    """
    with open(FILE_PATH) as f:
        data = json.load(f)
    if ARCHIVAL_KEY not in data \
            or HOUR_KEY not in data[ARCHIVAL_KEY] \
            or MINUT_KEY not in data[ARCHIVAL_KEY] \
            or not isTimeFormat(str(data[ARCHIVAL_KEY][HOUR_KEY])  +  ":"  +  str(data[ARCHIVAL_KEY][MINUT_KEY])):
        set_archival_job_config(HOUR_DEFAULT, MINUT_DEFAULT)
        data[ARCHIVAL_KEY] = {
            HOUR_KEY: HOUR_DEFAULT,
            MINUT_KEY: MINUT_DEFAULT
        }
    return data[ARCHIVAL_KEY]

def get_sqlalchemy_config():
    with open(FILE_PATH) as f:
        data = json.load(f)
    return data[SQL_URI_KEY], data[SQL_TRACK_KEY]

def set_archival_job_config(hour, minut):
    with open(FILE_PATH) as f:
        data = json.load(f)
    settings = {
        HOUR_KEY: hour,
        MINUT_KEY: minut
    }
    data[ARCHIVAL_KEY] = settings
    with open(FILE_PATH, 'w') as f:
        json.dump(data, f, indent=2)

def run_default_job():
    config = get_archival_config()
    __run_job(config[HOUR_KEY], config[MINUT_KEY])

def run_specific_job(hour, minut):
    if not isTimeFormat(str(hour) + ":" + str(minut)):
        timer = get_archival_config()
        hour = timer[HOUR_KEY]
        minut = timer[MINUT_KEY]
    set_archival_job_config(hour, minut)
    __run_job(hour, minut)

def __run_job(hour, minut):
    for job in scheduler.get_jobs():
        job.remove()
    scheduler.add_job(archival_job, "cron", hour=hour, minute=minut)
    if scheduler.state != STATE_RUNNING:
        scheduler.start()

def archival_job():
    sql_config = get_sqlalchemy_config()
    app = Flask(__name__)
    app.config[SQL_URI_KEY] = sql_config[0]
    app.config[SQL_TRACK_KEY] = sql_config[1]
    with app.app_context():
        db.init_app(app)
        toArchive = db.session.query(Publishing)\
            .filter(Publishing.date_until < datetime.now(), Publishing.state == 1)\
            .all()

        for pub in toArchive:
            pub.state = 2

        db.session.commit()

@archival_page.route('/set_new_archival_job', methods=['GET', 'POST'])
@login_required(admin_required=True)
def new_archival_job():
    if request.method == 'POST':
        timer = request.form['arch_time']
        if not isTimeFormat(timer):
            return redirect(url_for('posts.records'))
        timer = timer.split(":")
        hour = int(timer[0])
        minut = int(timer[1])
        run_specific_job(hour, minut)
    return redirect(url_for('posts.records'))

@archival_page.route('/update_archival_states', methods=['GET', 'POST'])
@login_required(admin_required=True)
def update_now():
    archival_job()
    return redirect(url_for('posts.records'))

def isTimeFormat(input):
    try:
        time.strptime(input, '%H:%M')
        return True
    except ValueError:
        return False
