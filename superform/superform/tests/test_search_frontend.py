from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from sqlalchemy.exc import InvalidRequestError

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
    id_channels = [0, -1, -2]
    id_posts = [0, -1, -2]
    channel = Channel(id=id_channels[0], name="Test_channel_1", module="superform.plugins.Twitter", config="{}")
    db.session.add(channel)
    channel = Channel(id=id_channels[1], name="Test_channel_2", module="superform.plugins.Twitter", config="{}")
    db.session.add(channel)
    channel = Channel(id=id_channels[2], name="Test_channel_3", module="superform.plugins.Twitter", config="{}")
    db.session.add(channel)

    authorization = Authorization(user_id="myself", channel_id=id_channels[0], permission=2)

    db.session.add(authorization)

    post = Post(id=id_posts[0], user_id="myself", title="first title #123456789123456789123456789title",
                description="This is a test, yes it really is. #123456789123456789123456789descr",
                link_url="http://facebook.com/", image_url="pas", date_from=datetime_converter("2018-08-08"),
                date_until=datetime_converter("2018-08-10"))
    db.session.add(post)

    publishing = Publishing(post_id=id_posts[0], channel_id=id_channels[0], state=0, title="first title #123456789123456789123456789title",
                            description="This is a test, yes it really is. #123456789123456789123456789descr",
                            link_url="http://facebook.com/", image_url="pas",
                            date_from=datetime_converter("2018-08-08"),
                            date_until=datetime_converter("2018-08-10"), extra="{}")
    db.session.add(publishing)
    publishing = Publishing(post_id=id_posts[0], channel_id=id_channels[1], state=0, title="first title #123456789123456789123456789title",
                            description="This is a test, yes it really is. #123456789123456789123456789descr",
                            link_url="http://facebook.com/", image_url="pas",
                            date_from=datetime_converter("2018-11-11"),
                            date_until=datetime_converter("2018-11-12"), extra="{}")
    db.session.add(publishing)

    try:
        db.session.commit()
    except:
        db.session.rollback()
    return id_channels, id_posts


def teardown_db(id_channels, id_posts):
    for id_post in id_posts:
        post = db.session.query(Post).filter(Post.id == id_post).first()
        for id_channel in id_channels:
            publishing = db.session.query(Publishing).filter(
                Publishing.post_id == id_post and Publishing.channel_id == id_channel).first()
            if publishing is not None:
                db.session.delete(publishing)
        if post is not None:
            db.session.delete(post)
    for id_channel in id_channels:
        channel = db.session.query(Channel).filter(Channel.id == id_channel).first()
        if channel is not None:
            db.session.delete(channel)
    try:
        db.session.commit()
    except:
        db.session.rollback()


class TestLiveServer:

    def test_basic(self, client):
        id_channels, id_posts = setup_db()
        driver = webdriver.Firefox()
        try:
            driver.get('http://127.0.0.1:5000/')
            driver.find_element_by_link_text("Login").click()
            driver.find_element_by_name("j_username").send_keys("myself")
            driver.find_element_by_name("j_password").send_keys("myself")
            driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Password:'])[1]/following::input[2]").click()
            wait = WebDriverWait(driver, 10)
            wait.until(EC.element_to_be_clickable((By.LINK_TEXT, 'Search')))
            driver.find_element_by_link_text("Search").click()
            driver.find_element_by_id("advanced_search_button").click()
            driver.find_element_by_xpath(
                "(.//*[normalize-space(text()) and normalize-space(.)='Searching fields'])[1]/following::input[3]").click()
            driver.find_element_by_id("search_word").send_keys("#123456789123456789123456789")
            driver.find_element_by_id("submit_search").click()

            table_results = driver.find_element_by_id("result_tab")
            rows = table_results.find_elements_by_tag_name("tr")
            assert len(rows) == 2
            cols = rows[1].find_elements_by_tag_name("td")
            assert len(cols) > 0
            assert cols[0].text == "0"

            driver.find_element_by_id("search_word").send_keys("#123456789123456789123456789title")
            driver.find_element_by_id("submit_search").click()

            table_results = driver.find_element_by_id("result_tab")
            rows = table_results.find_elements_by_tag_name("tr")
            assert len(rows) == 2
            cols = rows[1].find_elements_by_tag_name("td")
            assert len(cols) > 0
            assert cols[0].text == "0"

            driver.find_element_by_id("search_word").send_keys("#123456789123456789123456789descr")
            driver.find_element_by_id("submit_search").click()

            table_results = driver.find_element_by_id("result_tab")
            rows = table_results.find_elements_by_tag_name("tr")
            assert len(rows) == 2
            cols = rows[1].find_elements_by_tag_name("td")
            assert len(cols) > 0
            assert cols[0].text == "0"

            driver.find_element_by_id("search_word").send_keys("#123456789123456789123456789YOUPIDOU420")
            driver.find_element_by_id("submit_search").click()

            table_results = driver.find_element_by_id("result_tab")
            rows = table_results.find_elements_by_tag_name("tr")
            assert len(rows) == 1
        except AssertionError as e:
            teardown_db(id_channels, id_posts)
            driver.close()
            assert False, str(e)
        except InvalidRequestError as e:
            teardown_db(id_channels, id_posts)
            driver.close()
            assert False, "An error occured while testing: {}".format(str(e))
        teardown_db(id_channels, id_posts)
        driver.close()
        driver.close()

    def test_search_date(self, client):
        id_channels, id_posts = setup_db()
        driver = webdriver.Firefox()
        try:
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
            driver.find_element_by_xpath(
                "(.//*[normalize-space(text()) and normalize-space(.)='Searching fields'])[1]/following::input[3]").click()
            driver.find_element_by_id("date_from").send_keys("2018-08-07")
            driver.find_element_by_id("date_until").send_keys("2018-08-20")
            driver.find_element_by_id("search_word").send_keys("#123456789123456789123456789")
            driver.find_element_by_id("submit_search").click()

            table_results = driver.find_element_by_id("result_tab")
            rows = table_results.find_elements_by_tag_name("tr")
            assert len(rows) == 2
            cols = rows[1].find_elements_by_tag_name("td")
            assert len(cols) > 0
            assert cols[0].text == "0"

            driver.find_element_by_id("advanced_search_button").click()
            driver.find_element_by_id("date_from").send_keys("2018-08-11")
            driver.find_element_by_id("date_until").send_keys("2018-08-20")
            driver.find_element_by_id("search_word").send_keys("test")
            driver.find_element_by_id("submit_search").click()

            table_results = driver.find_element_by_id("result_tab")
            rows = table_results.find_elements_by_tag_name("tr")
            assert len(rows) == 1
        except AssertionError as e:
            teardown_db(id_channels, id_posts)
            driver.close()
            assert False, str(e)
        except InvalidRequestError as e:
            teardown_db(id_channels, id_posts)
            driver.close()
            assert False, "An error occured while testing: {}".format(str(e))

        teardown_db(id_channels, id_posts)
        driver.close()

    """
    def test_search_status(self, client):
        id_channels, id_posts = setup_db()
        driver = webdriver.Firefox()
        try:
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
        except AssertionError as e:
            teardown_db(id_channels, id_posts)
            driver.close()
            assert False, str(e)
        except Exception as e:
            teardown_db(id_channels, id_posts)
            driver.close()
            assert False, "An error occured while testing: {}".format(str(e))
        driver.close()
        teardown_db(id_channels, id_posts)
    """
    def test_search_searching_fields(self, client):
        id_channels, id_posts = setup_db()
        driver = webdriver.Firefox()
        try:
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
            driver.find_element_by_xpath(
                "(.//*[normalize-space(text()) and normalize-space(.)='Searching fields'])[1]/following::input[3]").click()
            driver.execute_script("$('#search_loc').val('title').trigger('change');")  # Title
            driver.find_element_by_id("search_word").send_keys("#123456789123456789123456789title")
            driver.find_element_by_id("submit_search").click()

            table_results = driver.find_element_by_id("result_tab")
            rows = table_results.find_elements_by_tag_name("tr")
            assert len(rows) == 2
            cols = rows[1].find_elements_by_tag_name("td")
            assert len(cols) > 0
            assert cols[0].text == "0"

            driver.find_element_by_id("advanced_search_button").click()
            driver.execute_script("$('#search_loc').val('description').trigger('change');")  # Description
            driver.find_element_by_id("submit_search").click()

            table_results = driver.find_element_by_id("result_tab")
            rows = table_results.find_elements_by_tag_name("tr")
            assert len(rows) == 1
        except AssertionError as e:
            teardown_db(id_channels, id_posts)
            driver.close()
            assert False, str(e)
        except Exception as e:
            teardown_db(id_channels, id_posts)
            driver.close()
            assert False, "An error occured while testing: {}".format(str(e))
        driver.close()
        teardown_db(id_channels, id_posts)

    """
    def test_search_order(self, client):
        id_channels, id_posts = setup_db()
        driver = webdriver.Firefox()
        try:
            driver.get('http://127.0.0.1:5000/')
            driver.find_element_by_link_text("Login").click()
            driver.find_element_by_name("j_username").send_keys("myself")
            driver.find_element_by_name("j_password").send_keys("myself")
            driver.find_element_by_xpath(
                "(.//*[normalize-space(text()) and normalize-space(.)='Password:'])[1]/following::input[2]").click()
            wait = WebDriverWait(driver, 10)
            wait.until(EC.element_to_be_clickable((By.LINK_TEXT, 'Search')))

        except AssertionError as e:
            teardown_db(id_channels, id_posts)
            driver.close()
            assert False, str(e)
        except Exception as e:
            teardown_db(id_channels, id_posts)
            driver.close()
            assert False, "An error occured while testing: {}".format(str(e))
        driver.close()
        teardown_db(id_channels, id_posts)"""