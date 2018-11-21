import os
import tempfile
import json
import pytest
import facebook

from superform import app, db
from superform.models import Publishing, Channel
from superform.plugins import facebook as fb


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


def test_config(client):

    assert fb.get_config("12121212121", "333333") == {"page_id": "12121212121",
                                 "access_token": "333333"}


def test_publish_msg(client):

    new_publish = Publishing(title="Coucou", description="J'aime faire des tests unitaires", link_url="https://docs.pytest.org/en/latest/index.html")

    assert fb.get_message(new_publish) == "Coucou\n\nJ'aime faire des tests unitaires"


def test_publish_link(client):

    new_publish = Publishing(title="Coucou", description="J'aime faire des tests unitaires", link_url="https://docs.pytest.org/en/latest/index.html")

    assert fb.get_link(new_publish) == "https://docs.pytest.org/en/latest/index.html"

