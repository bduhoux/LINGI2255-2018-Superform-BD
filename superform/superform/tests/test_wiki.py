import os
import tempfile
import json
import pytest
import urllib.error

from urllib.parse import urlencode
from urllib.request import Request, urlopen
from superform import app, db
from superform.models import Channel


new_channel_config = "{\"Author\": \"myself\", \"Wiki's url\": \"http://localhost:8001/pmwiki.php\", \"Publication's group\": \"Test\"}"
channel = Channel(name="newWikiChannel", module="superform.plugins.wiki", config=new_channel_config)


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


def test_wiki_create(client):
    create_channel()
    url = get_url_wiki()
    post_fields = {'n': "Test.WikiDumbPageForTestingSuperform2018", 'text': "violet", 'action': 'edit', 'post': 1}
    request = Request(url, urlencode(post_fields).encode())
    response = urlopen(request)
    mybytes = response.read()
    mystr = mybytes.decode("utf8")
    response.close()

    expected_text = "violet"
    assert expected_text in mystr


def test_wiki_edit(client):
    url = get_url_wiki()
    post_fields = {'n': "Test.WikiDumbPageForTestingSuperform2018", 'text': "Magenta", 'action': 'edit', 'post': 1}
    request = Request(url, urlencode(post_fields).encode())
    response = urlopen(request)
    mybytes = response.read()
    mystr = mybytes.decode("utf8")
    response.close()

    not_expected_text = "violet"
    assert not_expected_text not in mystr
    expected_text = "Magenta"
    assert expected_text in mystr


def test_wiki_delete(client):
    url = get_url_wiki()
    post_fields = {'n': "Test.WikiDumbPageForTestingSuperform2018", 'text': "delete", 'action': 'edit', 'post': 1}
    request = Request(url, urlencode(post_fields).encode())
    with pytest.raises(urllib.error.HTTPError):
        urlopen(request)
    delete_channel()


def get_url(config):
    json_data = json.loads(config)
    return json_data["Wiki's url"]


def get_url_wiki():
    c = db.session.query(Channel).filter(Channel.id == channel.id).first()
    return get_url(c.config)


def create_channel():
    db.session.add(channel)
    db.session.commit()


def delete_channel():
    db.session.delete(channel)
    db.session.commit()
