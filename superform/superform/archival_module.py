import os
from superform.models import db, Publishing
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from superform.utils import login_required
import json, time
from flask import Blueprint, url_for, redirect, request, Flask

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

scheduler = BackgroundScheduler()
scheduler.start()

def get_sqlalchemy_config():
    with open(FILE_PATH) as f:
        data = json.load(f)
    return data[SQL_URI_KEY], data[SQL_TRACK_KEY]

def delete_job(ch_id):
    # TODO
    pass

def is_valid_data(data):
    if FORM_FREQ_KEY not in data \
            or FORM_DAY_KEY not in data \
            or FORM_HOUR_KEY not in data \
            or FORM_MONTH_KEY not in data\
            or not isTimeFormat(data[FORM_HOUR_KEY])\
            or not isNumberBetween(data[FORM_MONTH_KEY], 1, 29)\
            or not isNumberBetween(data[FORM_DAY_KEY], 1, 8)\
            or not isNumberBetween(data[FORM_FREQ_KEY], float('-inf'), float('inf')) \
            or int(data[FORM_FREQ_KEY]) not in FREQUENCIES:
        return False
    return True

def configure_job(ch_id, data):
    if not is_valid_data(data):
        return None

    freq = int(data[FORM_FREQ_KEY])
    date = datetime.today()

    if freq == -1:
        delete_job(ch_id)
        return (freq, date)

    timer = data[FORM_HOUR_KEY].split(":")
    hour = int(timer[0])
    minute = int(timer[1])

    if freq == 0: # monthly
        scheduler.add_job(archival_job, trigger="cron", args=[ch_id], id=str(ch_id), replace_existing=True,
                              day=data[FORM_MONTH_KEY], hour=hour, minute=minute)
        date = datetime(2018, 1, int(data[FORM_MONTH_KEY]), hour, minute)
    elif freq == 1: # weekly
        day = int(data[FORM_DAY_KEY])
        date = datetime(2018, 1, day, hour, minute) # since January 1, 2018 is a Monday
        day -= 1
        scheduler.add_job(archival_job, trigger="cron", args=[ch_id], id=str(ch_id), replace_existing=True,
                              day_of_week=day, hour=hour, minute=minute)
    elif freq == 2: # daily
        date = datetime(2018, 1, 1, hour, minute)
        scheduler.add_job(archival_job, trigger="cron", args=[ch_id], id=str(ch_id), replace_existing=True,
                              hour=hour, minute=minute)
    return (freq, date)

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