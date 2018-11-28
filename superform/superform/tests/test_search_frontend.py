from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select

import pytest
import tempfile, os
from selenium import webdriver
from superform import db, app
from selenium.webdriver.support import expected_conditions as EC

from superform.models import Authorization, Channel, User, Post, Publishing
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

def setup_db():
    channel = Channel(id=-1, name="Twitter", module="superform.plugins.Twitter", config="{}")
    db.session.add(channel)

    authorization = Authorization(user_id="myself", channel_id=-1, permission=2)
    db.session.add(authorization)

    post = Post(id=-1, user_id="babelou", title="first title",
                description="That know ask case sex ham dear her spot. Weddings followed the all marianne nor whatever settling. Perhaps six prudent several her had offence. Did had way law dinner square tastes. Recommend concealed yet her procuring see consulted depending. Adieus hunted end plenty are his she afraid. Resources agreement contained propriety applauded neglected use yet. ",
                link_url="http://facebook.com/", image_url="pas", date_from=datetime_converter("2018-07-01"),
                date_until=datetime_converter("2018-07-01"))
    db.session.add(post)
    db.session.commit()


def teardown_db():
    post = db.session.query(Post).filter(Post.id == -1).first()
    channel = db.session.query(Channel).filter(Channel.id == -1).first()
    db.session.delete(post)
    db.session.delete(channel)
    db.session.commit()

class TestLiveServer:

    def test_basic(self):
        #setup_db()
        driver = webdriver.Firefox()
        driver.get('http://127.0.0.1:5000/')
        driver.find_element_by_link_text("Login").click()
        driver.find_element_by_name("j_username").send_keys("myself")
        driver.find_element_by_name("j_password").send_keys("myself")
        driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Password:'])[1]/following::input[2]").click()
        wait = WebDriverWait(driver, 10)
        wait.until(EC.element_to_be_clickable((By.LINK_TEXT, 'Search')))
        driver.find_element_by_link_text("Search").click()
        driver.find_element_by_id("search_word").send_keys("test")
        driver.find_element_by_id("submit_search").click()
        assert driver.title == 'Search - Superform', driver.title
        driver.close()
        #teardown_db()

    def test_search_date(self):
        #setup_db()
        driver = webdriver.Firefox()
        driver.get('http://127.0.0.1:5000/')
        driver.find_element_by_link_text("Login").click()
        driver.find_element_by_name("j_username").send_keys("myself")
        driver.find_element_by_name("j_password").send_keys("myself")
        driver.find_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)='Password:'])[1]/following::input[2]").click()
        wait = WebDriverWait(driver, 10)
        wait.until(EC.element_to_be_clickable((By.LINK_TEXT, 'Search')))
        driver.find_element_by_link_text("Search").click()
        driver.find_element_by_id("advanced_search_button").click()
        driver.find_element_by_id("date_from").send_keys("2018-12-01")
        driver.find_element_by_id("date_until").send_keys("2018-12-08")
        driver.find_element_by_id("search_word").send_keys("test")
        driver.find_element_by_id("submit_search").click()

        assert driver.title == 'Search - Superform', driver.title

        driver.close()
        #teardown_db()

    def test_search_status(self):
        # setup_db()
        driver = webdriver.Firefox()
        driver.get('http://127.0.0.1:5000/')
        driver.find_element_by_link_text("Login").click()
        driver.find_element_by_name("j_username").send_keys("myself")
        driver.find_element_by_name("j_password").send_keys("myself")
        driver.find_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)='Password:'])[1]/following::input[2]").click()
        wait = WebDriverWait(driver, 10)
        wait.until(EC.element_to_be_clickable((By.LINK_TEXT, 'Search')))
        driver.find_element_by_link_text("Search").click()
        driver.find_element_by_id("search_word").send_keys("Test")
        driver.find_element_by_id("advanced_search_button").click()
        driver.execute_script("$('#post_status').val('1').trigger('change');")  # Published

        driver.find_element_by_id("submit_search").click()
        assert driver.title == 'Search - Superform', driver.title
        driver.find_element_by_id("advanced_search_button").click()
        driver.execute_script("$('#post_status').val('0').trigger('change');")  # Waiting for approval

        driver.find_element_by_id("submit_search").click()
        assert driver.title == 'Search - Superform', driver.title
        driver.find_element_by_id("advanced_search_button").click()
        driver.execute_script("$('#post_status').val(['2', '1']).trigger('change');")  # Archived and Incomplete
        driver.find_element_by_id("submit_search").click()
        assert driver.title == 'Search - Superform', driver.title
        driver.close()
        # teardown_db()

    def test_search_searching_fields(self):
        # setup_db()
        driver = webdriver.Firefox()
        driver.get('http://127.0.0.1:5000/')
        driver.find_element_by_link_text("Login").click()
        driver.find_element_by_name("j_username").send_keys("myself")
        driver.find_element_by_name("j_password").send_keys("myself")
        driver.find_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)='Password:'])[1]/following::input[2]").click()
        wait = WebDriverWait(driver, 10)
        wait.until(EC.element_to_be_clickable((By.LINK_TEXT, 'Search')))
        driver.find_element_by_link_text("Search").click()
        driver.find_element_by_id("advanced_search_button").click()
        driver.execute_script("$('#search_loc').val('title').trigger('change');")  # Title
        driver.find_element_by_id("search_word").send_keys("test")
        driver.find_element_by_id("submit_search").click()
        assert driver.title == 'Search - Superform', driver.title
        driver.find_element_by_id("advanced_search_button").click()
        driver.execute_script("$('#search_loc').val('description').trigger('change');")  # Description
        driver.find_element_by_id("submit_search").click()
        assert driver.title == 'Search - Superform', driver.title
        driver.close()
        # teardown_db()

    def test_search_post(self):
        # setup_db()
        driver = webdriver.Firefox()
        driver.get('http://127.0.0.1:5000/')
        driver.find_element_by_link_text("Login").click()
        driver.find_element_by_name("j_username").send_keys("myself")
        driver.find_element_by_name("j_password").send_keys("myself")
        driver.find_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)='Password:'])[1]/following::input[2]").click()
        wait = WebDriverWait(driver, 10)
        wait.until(EC.element_to_be_clickable((By.LINK_TEXT, 'Search')))
        driver.find_element_by_link_text("Search").click()
        driver.find_element_by_id("search_word").send_keys("test")
        driver.find_element_by_id("advanced_search_button").click()
        driver.find_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)='Searching fields'])[1]/following::input[3]").click()
        driver.find_element_by_id("submit_search").click()
        driver.close()
        # teardown_db()


