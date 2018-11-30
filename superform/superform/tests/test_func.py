import os
import tempfile
import pytest
import time
import threading

from superform import app, db
from superform.models import Post, Publishing
from superform.utils import datetime_converter

from selenium import webdriver
from selenium.webdriver.common.by import By
from superform.models import db, Publishing, Channel

browser = webdriver.Chrome('/home/maitre/Downloads/chromedriver')
# browser = webdriver.Firefox('/home/maitre/Downloads/geckodriver')


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


def test_facebook_functional(client):
    assert True == True
    # threading.Thread(target=app.run, daemon=True).start() # stop serveur quand test est fini

    time.sleep(1)
    browser.get('http://localhost:5000/login')
    browser.maximize_window()
    #login_button = browser.find_element_by_link_text('Login')
    #login_button.click()
    browser.find_element_by_name("j_username").send_keys("myself")
    browser.find_element_by_name("j_password").send_keys("myself")
    browser.find_element(By.XPATH, "//input[@value='Login']").click()
    time.sleep(5)
    browser.find_element(By.XPATH, "//a[@href='/new']").click()
    #browser.get('http://localhost:5000/new')
    time.sleep(5)