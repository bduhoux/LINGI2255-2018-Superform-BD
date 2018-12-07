import os
import tempfile
import json
import pytest
import urllib.error

from urllib.parse import urlencode
from urllib.request import Request, urlopen
from superform import app, db, User, Post
from superform.models import Publishing, Channel
from superform.plugins import wiki

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


def get_url_wiki():
    c = db.session.query(Channel).filter(Channel.module == "superform.plugins.wiki").first()
    return get_url(c.config)


def test_wiki_create(client):
    url = get_url_wiki()
    post_fields = {'n': "PmWiki.WikiDumbPageForTestingSuperform2018", 'text': "violet", 'action': 'edit', 'post': 1}
    request = Request(url, urlencode(post_fields).encode())
    response = urlopen(request)
    mybytes = response.read()
    mystr = mybytes.decode("utf8")
    response.close()

    expected_text = "violet"
    assert expected_text in mystr


def test_wiki_edit(client):
    url = get_url_wiki()
    post_fields = {'n': "PmWiki.WikiDumbPageForTestingSuperform2018", 'text': "Magenta", 'action': 'edit', 'post': 1}
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
    post_fields = {'n': "PmWiki.WikiDumbPageForTestingSuperform2018", 'text': "delete", 'action': 'edit', 'post': 1}
    request = Request(url, urlencode(post_fields).encode())
    with pytest.raises(urllib.error.HTTPError):
        urlopen(request)


def get_url(config):
    json_data = json.loads(config)
    return json_data["Wiki's url"]
