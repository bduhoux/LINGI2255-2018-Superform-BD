import pytest
import datetime
import os
import tempfile

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
                sess["admin"] = False
            else:
                sess["admin"] = False

            sess["logged_in"] = True
            sess["first_name"] = "gen_login"
            sess["name"] = "myname_gen"
            sess["email"] = "hello@genemail.com"
            sess['user_id'] = login


def test_get_module_rss():
    """
    Tests if the module rss is active
    :return:
    """
    module_name = "rss"
    m = get_module_full_name(module_name)
    assert m == "superform.plugins.rss"


def test_channel_rss():
    """
    Creation of a channel named test
    :return:
    """
    channel = Channel.query.filter_by(
        module='superform.plugins.rss',
        name='test'
    ).first()

    assert channel is None

    channel = Channel(name="test", module=get_module_full_name("rss"), config="{}")
    db.session.add(channel)

    channel = Channel.query.filter_by(
        module='superform.plugins.rss',
        name='test'
    ).first()

    assert channel is not None

    assert channel.name == 'test'


def test_post_to_rss(client):
    """
    You must create a channel named RSS and give moderator permission to myself for the channel
    Posts a publication and verify if it's present in the rss feed
    :param client:
    :return:
    """

    login(client, "myself")

    data = client.get('/rss.xml').data.decode("utf-8")

    assert 'Test of rss' not in data
    assert 'RSS feed' not in data

    """
    rv = client.post('/post', data=dict(title="Test of rss",
                                           description="RSS feed",
                                           link_url="http://www.test.com",
                                           image_url="image.jpg",
                                           date_from=datetime.date(2018, 1, 1),
                                           date_until=datetime.date(2019, 7, 1),
                                           datefrompost=datetime.date(2018, 1, 1),
                                           dateuntilpost=datetime.date(2019, 7, 1),
                                           titlepost='Test of rss',
                                           descrpost="RSS feed",
                                           linkurlpost="http://www.test.com",
                                           imagepost="image.jpg"
                                           )
                     )

    post = Post.query.filter_by(
        title='Test of rss',
        description="RSS feed"
    ).first()

    print(post.id)
    """

    rv = client.post('/publish', data=dict(title="Test of rss",
                                           description="RSS feed",
                                           # post_id=post.id,
                                           channel_id=3,
                                           link_url="http://www.test.com",
                                           image_url="image.jpg",
                                           date_from=datetime.date(2018, 1, 1),
                                           date_until=datetime.date(2019, 7, 1),
                                           datefrompost=datetime.date(2018, 1, 1),
                                           dateuntilpost=datetime.date(2019, 7, 1),
                                           titlepost='Test of rss',
                                           descrpost="RSS feed",
                                           linkurlpost="http://www.test.com",
                                           imagepost="image.jpg",
                                           chan_option_={'name': 'RSS'}  # What The fuck here ?? TODO
                                           )
                     )

    assert rv.status_code == 302

    data = client.get('/rss.xml').data.decode("utf-8")

    print(data)

    assert 'Test of rss' in data
    assert 'RSS feed' in data
