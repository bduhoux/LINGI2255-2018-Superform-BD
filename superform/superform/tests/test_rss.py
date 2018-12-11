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


def get_dict_publish(title, description, link_url, image_url, datefrom, dateuntil, channel_name):
    """
    Return a dictionary ready to send as data for publishing
    :param title:
    :param description:
    :param link_url:
    :param image_url:
    :param datefrom:
    :param dateuntil:
    :param channel_name:
    :return:
    """
    channel = Channel.query.filter_by(name=channel_name).first()

    data_publish = {
        "title": title,
        "description": description,
        "channel_id": channel.id,
        "link_url": link_url,
        "image_url": image_url,
        "date_from": datefrom,
        "date_until": dateuntil,
        "datefrompost": datefrom,
        "dateuntilpost": dateuntil,
        "titlepost": title,
        "descriptionpost": description,
        "linkurlpost": link_url,
        "imagepost": image_url,
        "chan_option_{}".format(channel.id): '',
        "{}_datefrompost".format(channel_name): datefrom,
        "{}_dateuntilpost".format(channel_name): dateuntil,
    }

    return data_publish


def moderate_pub(data_publish, client):
    """
    Confirm the publication and send it to the rss
    :param data_publish:
    :param client:
    :return:
    """
    publishing = Publishing.query.filter_by(channel_id=data_publish['channel_id'], title=data_publish['title'],
                                            state=0).first()

    return client.post("/moderate/{}/{}".format(publishing.post_id, data_publish['channel_id']), data=dict(
        titlepost=data_publish['title'],
        descrpost=data_publish['description'],
        linkurlpost=data_publish['link_url'],
        imagepost=data_publish['image_url'],
        datefrompost=data_publish['date_from'],
        dateuntilpost=data_publish['date_until']
    ))

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


@pytest.fixture(autouse=True)
def login_myself(client):
    login(client, "myself")


def test_get_module_rss():
    """
    Tests if the module rss is active
    :return:
    """
    module_name = "rss"
    m = get_module_full_name(module_name)
    assert m == "superform.plugins.rss"


def test_post_to_rss(client):
    """
    You must create a channel named RSS and give moderator permission to myself for the channel
    Posts a publication and verify if it's present in the rss feed
    :param client:
    :return:
    """
    data = client.get('/rss.xml').data.decode("utf-8")

    data_publish = get_dict_publish('Test of rss', 'RSS feed', 'http://www.test.com', 'image.jpg',
                                    datetime.date(2018, 1, 1), datetime.date(2019, 7, 1), 'RSS')

    client.post('/publish', data=data_publish)

    moderate_pub(data_publish, client)

    data = client.get('/rss.xml').data.decode("utf-8")

    assert 'Test of rss' in data
    assert 'RSS feed' in data


def test_post_to_rss_same_date(client):
    """
    You must create a channel named RSS and give moderator permission to myself for the channel
    Posts a publication and verify if it's present in the rss feed IF the date from is the same of date until
    :param client:
    :return:
    """
    data = client.get('/rss.xml').data.decode("utf-8")

    data_publish = get_dict_publish('Test of rss same date', 'RSS feed same date', 'http://www.test.com', 'image.jpg',
                                    datetime.datetime.now().date(), datetime.datetime.now().date(), 'RSS')

    client.post('/publish', data=data_publish)

    moderate_pub(data_publish, client)

    data = client.get('/rss.xml').data.decode("utf-8")

    assert 'Test of rss same date' in data
    assert 'RSS feed same date' in data
