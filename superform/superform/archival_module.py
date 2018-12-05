import os
from superform.models import db, Publishing
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from superform.utils import login_required
import json, time
from flask import Blueprint, url_for, redirect, request, Flask
from models import Channel

archival_page = Blueprint('archival', __name__)

FILE_PATH = os.path.dirname(os.path.abspath(__file__)) + '/config.json'
SQL_URI_KEY = "SQLALCHEMY_DATABASE_URI"
SQL_TRACK_KEY = "SQLALCHEMY_TRACK_MODIFICATIONS"

FORM_FREQ_KEY = 'arch_frequency'
FORM_MONTH_KEY = 'arch_date_month'
FORM_DAY_KEY = 'arch_date_week'
FORM_HOUR_KEY = 'arch_date_hour'

FREQUENCIES = {
    -1: 'None',
    0: 'Monthly',
    1: 'Weekly',
    2: 'Daily'
}

DEFAULT_FREQUENCY = 2 # Daily
DEFAULT_DATE = datetime(2018, 1, 1, 0, 0) # 2018/01/01 (Monday) 00:00

scheduler = BackgroundScheduler()
scheduler.start()

def get_sqlalchemy_config():
    with open(FILE_PATH) as f:
        data = json.load(f)
    return data[SQL_URI_KEY], data[SQL_TRACK_KEY]

def delete_job(ch_id):
    job = scheduler.get_job(str(ch_id))
    if job:
        job.remove()

def is_valid_data(data):
    if FORM_FREQ_KEY not in data \
            or FORM_DAY_KEY not in data \
            or FORM_HOUR_KEY not in data \
            or FORM_MONTH_KEY not in data\
            or not isTimeFormat(data[FORM_HOUR_KEY])\
            or not isNumberBetween(data[FORM_MONTH_KEY], 1, 32)\
            or not isNumberBetween(data[FORM_DAY_KEY], 1, 8)\
            or not isNumberBetween(data[FORM_FREQ_KEY], float('-inf'), float('inf')) \
            or int(data[FORM_FREQ_KEY]) not in FREQUENCIES:
        return False
    return True

def start_jobs_from_db():
    sql_config = get_sqlalchemy_config()
    app = Flask(__name__)
    app.config[SQL_URI_KEY] = sql_config[0]
    app.config[SQL_TRACK_KEY] = sql_config[1]
    with app.app_context():
        db.init_app(app)
        channels = db.session.query(Channel).all()
        for ch in channels:
            configure_job(ch.id, ch.archival_frequency, ch.archival_date)

def configure_job(ch_id, freq, date):
    if not isinstance(freq, int) \
            or freq not in FREQUENCIES \
            or not isinstance(date, datetime):
        return None

    if freq == -1: # none
        delete_job(ch_id)
        return (freq, date)

    if freq == 0: # monthly
        scheduler.add_job(archival_job, trigger="cron", args=[ch_id], id=str(ch_id), replace_existing=True,
                              day=date.day, hour=date.hour, minute=date.minute)
    elif freq == 1: # weekly
        day = date.weekday()
        scheduler.add_job(archival_job, trigger="cron", args=[ch_id], id=str(ch_id), replace_existing=True,
                              day_of_week=day, hour=date.hour, minute=date.minute)
    elif freq == 2: # daily
        scheduler.add_job(archival_job, trigger="cron", args=[ch_id], id=str(ch_id), replace_existing=True,
                              hour=date.hour, minute=date.minute)
    return (freq, date)

def configure_job_from_form(ch_id, data):
    if not is_valid_data(data):
        return None

    freq = int(data[FORM_FREQ_KEY])

    if freq == -1:
        return configure_job(ch_id, freq, datetime.today())

    timer = data[FORM_HOUR_KEY].split(":")
    hour = int(timer[0])
    minute = int(timer[1])

    if freq == 1: # weekly
        date = datetime(2018, 1, int(data[FORM_DAY_KEY]), hour, minute)  # since January 1, 2018 is a Monday
    else: # daily, monthly
        date = datetime(2018, 1, int(data[FORM_MONTH_KEY]), hour, minute)  # since January has 31 days

    return configure_job(ch_id, freq, date)

def archival_job(ch_id):
    sql_config = get_sqlalchemy_config()
    app = Flask(__name__)
    app.config[SQL_URI_KEY] = sql_config[0]
    app.config[SQL_TRACK_KEY] = sql_config[1]
    with app.app_context():
        db.init_app(app)
        if ch_id == -1:
            toArchive = db.session.query(Publishing)\
                .filter(Publishing.date_until < datetime.now(), Publishing.state == 1)\
                .all()
        else:
            toArchive = db.session.query(Publishing) \
                .filter(Publishing.date_until < datetime.now(), Publishing.state == 1, Publishing.channel_id == ch_id) \
                .all()

        for pub in toArchive:
            pub.state = 2

        db.session.commit()


@archival_page.route('/update_archival_states', methods=['GET', 'POST'])
@login_required(admin_required=True)
def update_now():
    archival_job(-1)
    return redirect(url_for('posts.records'))

def isTimeFormat(input):
    try:
        time.strptime(input, '%H:%M')
        return True
    except ValueError:
        return False

def isNumberBetween(s, a, b):
    # check if a <= int(s) < b
    try:
        i = int(s)
        return a <= i and i < b
    except ValueError:
        return False