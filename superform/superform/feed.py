from datetime import date, datetime

from feedgen.feed import FeedGenerator
from flask import Blueprint, url_for, request, redirect, render_template, session

from superform.utils import login_required, datetime_converter, str_converter
from superform.models import db, Publishing

feed_page = Blueprint('feed', __name__)


@feed_page.route('/rss.xml', methods=['GET'])
def rss_feed():
    # SQLAlchemy wants datetime objects (not date) when comparing db.DateTime objects,
    # so we convert today's date to a datetime object.
    now = datetime(*date.today().timetuple()[:3])

    publishings = db.session.query(Publishing).filter(
        Publishing.channel.has(module='superform.plugins.rss'),
        Publishing.state == 1,  # validated/shared
        Publishing.date_from <= now,
        now <= Publishing.date_until,
    ).all()

    feed = FeedGenerator()
    feed.title('Superform')
    feed.link(href='http://localhost:5000')
    feed.description('Superform')

    for publishing in publishings:
        entry = feed.add_entry()
        entry.title(publishing.title)
        entry.description(publishing.description)
        entry.link(href=publishing.link_url)

    return feed.rss_str(pretty=True)
