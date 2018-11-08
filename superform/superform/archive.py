from datetime import datetime
from superform.models import db
from apscheduler.schedulers.background import BackgroundScheduler

def update_state():
    expired = db.session.query(Post).filter()

scheduler = BackgroundScheduler()
scheduler.add_job(func=update_state, trigger="interval", seconds=3)
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())