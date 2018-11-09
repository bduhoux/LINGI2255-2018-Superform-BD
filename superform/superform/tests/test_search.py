import pytest
import os
import tempfile
from superform import app, db


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

def populate_db():
    pass


def test_basic_search():
    pass

def test_advanced_search():
    pass

def test_sql_injections():
    """
    Check if the search module prevents SQL injections:
        - Get publications from all users instead of only this user's
    :return:
    """
    pass