import os
import tempfile
import pytest
import time
from superform.tests.func_util import create_post, login, publish_fb, login_fb


from superform import app

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from superform.models import db, Publishing, Post

web_driver_location = os.getcwd() + '/superform/static/plugins/facebook/chromedriver'
driver = webdriver.Chrome(web_driver_location)


@pytest.fixture
def client():
    app.app_context().push()
    db_fd, app.config['DATABASE'] = tempfile.mkstemp() # database = database au path retourné
    app.config['TESTING'] = True
    client = app.test_client()

    with app.app_context():
        db.create_all()

    yield client

    os.close(db_fd)
    os.unlink(app.config['DATABASE'])

def get_time_string(date):
    if date.month < 10:
        month = "0" + str(date.month)
    else:
        month = str(date.month)
    if date.day < 10:
        day = "0" + str(date.day)
    else:
        day = str(date.day)
    year = str(date.year)
    return month + day + year

def test_facebook_functional(client):
    assert True == True
    login(driver)


    create_post(driver, "test", "test fonctionnel delete")
    time.sleep(2)
    pub_id = db.session.query(Publishing).order_by(Publishing.post_id.desc()).first().post_id
    driver.get('http://localhost:5000/delete/' + str(pub_id))
    time.sleep(2)
    driver.get('http://localhost:5000/delete_publishing/' + str(pub_id) + '/1')
    time.sleep(2)
    try:
        driver.switch_to.active_element().send_keys(Keys.ENTER)
    except(TypeError):
        pass

    time.sleep(2)
    create_post(driver, "test", "test fonctionnel delete supprimer post sur facebook")
    time.sleep(2)
    pub_id = publish_fb(driver)

    driver.get('https://www.facebook.com/pg/Test-453122048545115/posts/?ref=page_internal')
    time.sleep(10)

    driver.get('http://localhost:5000')
    time.sleep(1)
    driver.get('http://localhost:5000/delete/' + str(pub_id))

    login_fb(driver)

    driver.get('http://localhost:5000/delete_publishing/' + str(pub_id) + '/1')
    time.sleep(2)
    try:
        driver.switch_to.active_element().send_keys(Keys.ENTER)
    except:
        pass
    driver.get('https://www.facebook.com/pg/Test-453122048545115/posts/?ref=page_internal')





