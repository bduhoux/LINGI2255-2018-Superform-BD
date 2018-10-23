import datetime
import os
import tempfile

import pytest
from superform.utils import datetime_converter, str_converter, get_module_full_name
from superform import app, db, Post, User
from superform.models import Authorization, Channel
from superform.users import is_moderator, get_moderate_channels_for_user, channels_available_for_user
from superform.feed import rss_feed
from superform.models import db, Publishing, Channel


@pytest.fixture
def client():
    app.app_context().push()
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['TESTING'] = True
    client = app.test_client()

    with app.app_context():
        db.create_all()

    yield client

    os.close(db_fd)
    os.unlink(app.config['DATABASE'])


def login(client, login):
    with client as c:
        with c.session_transaction() as sess:
            if login is not "myself":
                sess["admin"] = True
            else:
                sess["admin"] = False

            sess["logged_in"] = True
            sess["first_name"] = "gen_login"
            sess["name"] = "myname_gen"
            sess["email"] = "hello@genemail.com"
            sess['user_id'] = login


def test_get_module_rss():
    module_name = "rss"
    m = get_module_full_name(module_name)
    assert m == "superform.plugins.rss"


def test_channel_rss():
    """
    For the sake of this test, you must erase all the channels with rss
    :return:
    """
    channel = Channel.query.filter_by(
        module='superform.plugins.rss',
    ).first()

    #assert channel is None

    channel = Channel(name="test", module=get_module_full_name("rss"), config="{}")
    db.session.add(channel)

    channel = Channel.query.filter_by(
        module='superform.plugins.rss'
    ).first()

    #assert channel is not None

    assert channel.name == 'test'


def test_post_to_rss():
    channel = Channel.query.filter_by(
        module='superform.plugins.rss',
        id=1
    ).first()

    login(client, "alterego")
    rv = client.post('/publish', data=dict(title='Test of rss', description="RSS feed",
                                           link_url="http://www.test.com", image_url="image.jpg",
                                           date_from="2018-07-01", date_until="2019-07-01", channel_id=1))

    assert rv.status_code == 302