import os
import tempfile

import pytest

from superform import app, db
from superform.models import Publishing, Channel
from superform.plugins import facebook


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


def test_run_facebook(client):
    new_channel = Channel(config={"page_id": "453122048545115",
                                  "access_token": "EAAEg6h9DvQwBADFqgmWtCnqXKXTFZAxxxIUHH3iZBHyj54pTYdykE39JQHhM9yOgFOigGCd3FZCqZCZA6wsmPUX7fGyea4Mso6aZBSvmGUZAjWKLzTSZCLZBHVfUtDRYKKNqcZA4Qe5JLzeaZC2THwERHrsTEZBHfHueHZBETYxBHCrZAmiajhFlki3SLZA"})

    assert facebook.get_page_id(new_channel.config) == "453122048545115"

    assert facebook.get_access_token(
        new_channel.config) == "EAAEg6h9DvQwBADFqgmWtCnqXKXTFZAxxxIUHH3iZBHyj54pTYdykE39JQHhM9yOgFOigGCd3FZCqZCZA6wsmPUX7fGyea4Mso6aZBSvmGUZAjWKLzTSZCLZBHVfUtDRYKKNqcZA4Qe5JLzeaZC2THwERHrsTEZBHfHueHZBETYxBHCrZAmiajhFlki3SLZA"

    assert facebook.get_config(facebook.get_page_id(new_channel.config), facebook.get_access_token(new_channel.config)) == {"page_id": "453122048545115",
                                  "access_token": "EAAEg6h9DvQwBADFqgmWtCnqXKXTFZAxxxIUHH3iZBHyj54pTYdykE39JQHhM9yOgFOigGCd3FZCqZCZA6wsmPUX7fGyea4Mso6aZBSvmGUZAjWKLzTSZCLZBHVfUtDRYKKNqcZA4Qe5JLzeaZC2THwERHrsTEZBHfHueHZBETYxBHCrZAmiajhFlki3SLZA"}

    new_publish = Publishing(title="Coucou", description="J'aime faire des tests unitaires", link_url="https://docs.pytest.org/en/latest/index.html")

    assert facebook.get_message(new_publish) == "Coucou\n\nJ'aime faire des tests unitaires"

    assert facebook.get_link(new_publish) == "https://docs.pytest.org/en/latest/index.html"