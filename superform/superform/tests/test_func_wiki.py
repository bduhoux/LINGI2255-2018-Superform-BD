import os
import tempfile
import pytest
import time
from superform.tests.func_util import create_post, create_post_wiki, login, publish_wiki


from superform import app
from selenium import webdriver
from selenium.webdriver.common.by import By
from superform.models import db, Publishing, Post

web_driver_location = os.getcwd() + '/superform/static/plugins/facebook/chromedriver'
#web_driver_location = os.getcwd() + '/superform/superform/static/plugins/facebook/chromedriver'



driver = webdriver.Chrome(web_driver_location)
# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("--incognito")
#driver = webdriver.Chrome(web_driver_location, chrome_options)



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

@pytest.mark.bug
def test_wiki_functional(client):
    assert True == True
    login(driver)
    post_title = "test"


    create_post_wiki(driver, post_title, "test fonctionnel delete unpublished post de wiki", 'superform.plugins.wiki')
    time.sleep(4)
    pub_id = db.session.query(Publishing).order_by(Publishing.post_id.desc()).first().post_id
    driver.get('http://localhost:5000/delete/' + str(pub_id))
    time.sleep(2)
    driver.find_element(By.XPATH, "//a[@role='button']").click()
    time.sleep(2)

    create_post_wiki(driver, "test", "test fonctionnel delete post de wiki", 'superform.plugins.wiki')


    time.sleep(2)
    pub_id = publish_wiki(driver)
    time.sleep(2)
    driver.get('http://localhost:8001/pmwiki.php')
    driver.find_element_by_name("q").send_keys(post_title)
    driver.find_element_by_class_name("inputbutton").click()
    time.sleep(2)
    driver.get('http://localhost:8001/pmwiki.php?n=PmWiki.' + post_title)
    time.sleep(2)
    driver.get('http://localhost:5000')


    driver.get('http://localhost:5000/delete/' + str(pub_id))
    time.sleep(2)
    driver.find_element(By.XPATH, "//a[@role='button']").click()
    time.sleep(2)


    driver.get('http://localhost:8001/pmwiki.php')
    driver.find_element_by_name("q").send_keys(post_title)
    driver.find_element_by_class_name("inputbutton").click()

