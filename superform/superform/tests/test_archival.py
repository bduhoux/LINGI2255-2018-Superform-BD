import datetime
import os
import tempfile

import pytest

from superform import app, db
from superform.archival_module import archival_job
from superform.models import Channel, Publishing
from superform.users import is_moderator, get_moderate_channels_for_user, channels_available_for_user
from superform.utils import datetime_converter, str_converter, get_module_full_name



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


def test_archival_job(client):
    login(client, "myself")

    post_data = get_dict_publish(
        title='Archival test ' + str(datetime.datetime.now()),
        description='Test of the archival job',
        link_url='https://example.com/',
        image_url='https://example.com/foo.png',
        datefrom=datetime.datetime.now().date(),
        dateuntil=datetime.datetime.now().date(),
        channel_name='RSS',
    )
    client.post('/publish', data=post_data)

    assert post_data['title'] not in client.get('/records').data.decode()

    moderate_pub(post_data, client)
    publishing = Publishing.query.filter_by(title=post_data['title']).first()
    publishing.date_from = publishing.date_from - datetime.timedelta(days=7)
    publishing.date_until = publishing.date_until - datetime.timedelta(days=7)
    db.session.commit()
    archival_job(publishing.channel_id)

    assert post_data['title'] in client.get('/records').data.decode()

