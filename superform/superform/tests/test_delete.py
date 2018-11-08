import os
import tempfile
import pytest

from superform import app, db, delete
from superform.models import Post
from superform.utils import datetime_converter

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


def test_delete_publish():
    user_id = 1
    title_post = "title_test"
    descr_post = "description"
    link_post = "link"
    image_post = "img"
    date_from = datetime_converter("2018-01-01")
    date_until = datetime_converter("2018-01-10")
    p = Post(user_id=user_id, title=title_post, description=descr_post, link_url=link_post, image_url=image_post,
             date_from=date_from, date_until=date_until)
    db.session.add(p)

    id_post = p.id

    delete.delete_post(id_post)
    deleted_post = db.session.query(Post).get(id_post)
    assert deleted_post is None
