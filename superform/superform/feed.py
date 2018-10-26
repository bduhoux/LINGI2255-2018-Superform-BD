from datetime import datetime

from feedgen.feed import FeedGenerator
from flask import Blueprint, url_for, request, redirect, render_template, session

from superform.utils import login_required, datetime_converter, str_converter
from superform.models import db, Publishing, Channel

feed_page = Blueprint('feed', __name__)


@feed_page.route('/rss.xml', methods=['GET'])
def rss_feed():
    now = datetime.now().date()

    publishings = db.session.query(Publishing).filter(
        Publishing.channel.has(module='superform.plugins.rss'),
        Publishing.state == 1,  # validated/shared

        # XXX: Doesn't work properly when Publishing.date_from == now == Publishing.date_until.
        # Not sure why. Let's investigate later.
        # Publishing.date_from <= now,

        now <= Publishing.date_until,
    ).all()

    feed = FeedGenerator()
    feed.title('Superform')
    feed.link(href='http://localhost:5000')
    feed.description('Superform')

    for publishing in publishings:
        # HACK: only way we've found for now (see the query).
        if not publishing.date_from.date() <= now:
            continue

        entry = feed.add_entry()
        entry.title(publishing.title)
        entry.description(publishing.description)
        entry.link(href=publishing.link_url)

    return feed.rss_str(pretty=True)
