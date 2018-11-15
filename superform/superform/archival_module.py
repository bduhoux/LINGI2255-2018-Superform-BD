from superform.models import db, Publishing
from datetime import datetime

def archival_job():

    toArchive = db.session.query(Publishing)\
        .filter(Publishing.date_until < datetime.now(), Publishing.state == 1)\
        .all()

    for pub in toArchive:
        pub.state = 2

    db.session.commit()