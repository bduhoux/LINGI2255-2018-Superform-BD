import os
import tempfile
import pytest
import time
from datetime import datetime
from datetime import timedelta


from superform import app, db

from selenium import webdriver
from selenium.webdriver.common.by import By
from superform.models import db, Publishing, Channel

web_driver_location = os.getcwd() + '/superform/superform/static/plugins/facebook/chromedriver'
browser = webdriver.Chrome(web_driver_location)
# browser = webdriver.Chrome('/home/maitre/Downloads/chromedriver')


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
    time.sleep(1)
    browser.get('http://localhost:5000/login')
    browser.maximize_window()
    browser.find_element_by_name("j_username").send_keys("myself")
    browser.find_element_by_name("j_password").send_keys("myself")
    browser.find_element(By.XPATH, "//input[@value='Login']").click()
    time.sleep(1)
    browser.find_element(By.XPATH, "//a[@href='/new']").click()
    browser.find_element(By.XPATH, "//input[@id='titlepost']").send_keys("Title")
    browser.find_element(By.XPATH, "//textarea[@id='descriptionpost']").send_keys("This is the description")
    browser.find_element(By.XPATH, "//input[@data-module='superform.plugins.facebook']").click()

    now = datetime.now()
    browser.find_element(By.XPATH, "//input[@id='datefrompost']").click()
    browser.find_element(By.XPATH, "//input[@id='datefrompost']").send_keys(get_time_string(now))
    then = now + timedelta(days=3)
    browser.find_element(By.XPATH, "//input[@id='dateuntilpost']").click()
    browser.find_element(By.XPATH, "//input[@id='dateuntilpost']").send_keys(get_time_string(then))
    time.sleep(1)
    browser.find_element(By.XPATH, "//button[@id='publish-button']").click()

    pub_id = db.session.query(Publishing).order_by(Publishing.post_id.desc()).first().post_id
    browser.get('http://localhost:5000/moderate/' + str(pub_id) +'/1')
    time.sleep(1)
    browser.find_element(By.XPATH, "//button[@id='pub-button']").click()
    window_before = browser.window_handles[0]
    time.sleep(5)
    browser.find_element(By.CLASS_NAME, "fb_iframe_widget").click()
    time.sleep(2)
    window_after = browser.window_handles[1]
    browser.switch_to.window(window_after)
    browser.find_element(By.XPATH, "//input[@id='email']").send_keys("guiste10@hotmail.be")
    browser.find_element(By.XPATH, "//input[@id='pass']").send_keys("soft@123")
    browser.find_element(By.XPATH, "//input[@value='Log In']").click()
    #browser.switch_to.window(window_before)
    time.sleep(1)
    # browser.find_element(By.XPATH, "//button[@name='__CONFIRM__']").click()
    browser.switch_to.window(window_before)
    time.sleep(3)
    browser.find_element(By.XPATH, "//button[@id='pub-button']").click()
    time.sleep(3)
    browser.find_element(By.XPATH, "//button[@id='pub-button']").click()
    time.sleep(3)
    browser.get('https://www.facebook.com/pg/Test-453122048545115/posts/?ref=page_internal')




