import json
import os

import tempfile

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import pytest
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
    id_channel = 0  # randint(0, 99999999999999)
    # while db.session.query(Channel).filter(Channel.id == id_channel).first() is not None:
    #    id_channel = randint(0, 99999999999999)

    channel = Channel(id=id_channel, name="Slack", module="superform.plugins.slack", config="{}")
    db.session.add(channel)
    authorization = Authorization(user_id="myself", channel_id=id_channel, permission=2)
    db.session.add(authorization)

    id_post = 0  # randint(0, 99999999999999)
    # while db.session.query(Post).filter(Post.id == id_post).first() is not None:
    #    id_post = randint(0, 99999999999999)

    post = Post(id=id_post, user_id="myself", title="first title",
                description="That know ask case sex ham dear her spot. Weddings followed the all marianne nor whatever settling. Perhaps six prudent several her had offence. Did had way law dinner square tastes. Recommend concealed yet her procuring see consulted depending. Adieus hunted end plenty are his she afraid. Resources agreement contained propriety applauded neglected use yet. ",
                link_url="http://facebook.com/", image_url="pas", date_from=datetime_converter("2018-07-01"),
                date_until=datetime_converter("2018-07-01"))
    db.session.add(post)

    db.session.commit()
    return id_channel, id_post


def teardown_db(id_channel, id_post):
    post = db.session.query(Post).filter(Post.id == id_post).first()
    channel = db.session.query(Channel).filter(Channel.id == id_channel).first()
    publishing = db.session.query(Publishing).filter(
        Publishing.post_id == id_post and Publishing.channel_id == id_channel).first()
    if publishing is not None:
        db.session.delete(publishing)
    db.session.delete(post)
    db.session.delete(channel)
    db.session.commit()


class TestLiveServer:
    def test_basic(self, client):
        try:
            id_channel, id_post = setup_db()
            driver = webdriver.Firefox()
            driver.get('http://127.0.0.1:5000/')
            wait = WebDriverWait(driver, 10)
            driver.find_element_by_link_text("Login").click()
            driver.find_element_by_name("j_username").click()
            driver.find_element_by_name("j_username").clear()
            driver.find_element_by_name("j_username").send_keys("myself")
            driver.find_element_by_name("j_password").click()
            driver.find_element_by_name("j_password").clear()
            driver.find_element_by_name("j_password").send_keys("myself")
            driver.find_element_by_xpath(
                "(.//*[normalize-space(text()) and normalize-space(.)='Password:'])[1]/following::input[2]").click()
            wait = WebDriverWait(driver, 10)
            wait.until(EC.element_to_be_clickable((By.LINK_TEXT, 'New post')))
            driver.find_element_by_link_text("New post").click()
            driver.find_element_by_id("chan_option_" + str(id_channel)).click()
            driver.find_element_by_id("titlepost").click()
            driver.find_element_by_id("titlepost").clear()
            driver.find_element_by_id("titlepost").send_keys("Test")
            driver.find_element_by_id("descriptionpost").click()
            driver.find_element_by_id("descriptionpost").clear()
            driver.find_element_by_id("descriptionpost").send_keys(
                "Frontend")
            driver.find_element_by_id("linkurlpost").click()
            driver.find_element_by_id("linkurlpost").clear()
            driver.find_element_by_id("linkurlpost").send_keys("http://127.0.0.1:5000/new")
            driver.find_element_by_id("datefrompost").click()
            driver.find_element_by_id("datefrompost").clear()
            driver.find_element_by_id("datefrompost").send_keys("2020-11-21")
            driver.find_element_by_id("dateuntilpost").click()
            driver.find_element_by_id("dateuntilpost").clear()
            driver.find_element_by_id("dateuntilpost").send_keys("2021-01-29")
            driver.find_element_by_link_text("Slack").click()

            assert driver.find_element_by_id("Slack_titlepost").get_attribute(
                "value") == "Test"
            assert driver.find_element_by_id("Slack_descriptionpost").get_attribute(
                "value") == "Frontend"
            assert driver.find_element_by_id("Slack_linkurlpost").get_attribute(
                "value") == "http://127.0.0.1:5000/new"
            driver.close()
            teardown_db(id_channel, id_post)
        except Exception as e:
            driver.close()
            teardown_db(id_channel, id_post)
            assert False, e

    def test_basic_moderate(self, client):
        try:
            id_channel, id_post = setup_db()
            driver = webdriver.Firefox()
            driver.get('http://127.0.0.1:5000/')
            wait = WebDriverWait(driver, 10)
            driver.find_element_by_link_text("Login").click()
            driver.find_element_by_name("j_username").click()
            driver.find_element_by_name("j_username").clear()
            driver.find_element_by_name("j_username").send_keys("myself")
            driver.find_element_by_name("j_password").click()
            driver.find_element_by_name("j_password").clear()
            driver.find_element_by_name("j_password").send_keys("myself")
            driver.find_element_by_xpath(
                "(.//*[normalize-space(text()) and normalize-space(.)='Password:'])[1]/following::input[2]").click()
            wait = WebDriverWait(driver, 10)
            wait.until(EC.element_to_be_clickable((By.LINK_TEXT, 'New post')))
            driver.find_element_by_link_text("New post").click()
            driver.find_element_by_id("chan_option_" + str(id_channel)).click()
            driver.find_element_by_id("titlepost").click()
            driver.find_element_by_id("titlepost").clear()
            driver.find_element_by_id("titlepost").send_keys("Test")
            driver.find_element_by_id("descriptionpost").click()
            driver.find_element_by_id("descriptionpost").clear()
            driver.find_element_by_id("descriptionpost").send_keys(
                "Frontend")
            driver.find_element_by_id("linkurlpost").click()
            driver.find_element_by_id("linkurlpost").clear()
            driver.find_element_by_id("linkurlpost").send_keys("http://127.0.0.1:5000/new")
            driver.find_element_by_id("datefrompost").click()
            driver.find_element_by_id("datefrompost").clear()
            driver.find_element_by_id("datefrompost").send_keys("2020-11-21")
            driver.find_element_by_id("dateuntilpost").click()
            driver.find_element_by_id("dateuntilpost").clear()
            driver.find_element_by_id("dateuntilpost").send_keys("2021-01-29")
            driver.find_element_by_link_text("Slack").click()
            extra = {}
            pub = Publishing(post_id=id_post, channel_id=id_channel, state=0, title=driver.find_element_by_id("Slack_titlepost").get_attribute("value"),
                             description=driver.find_element_by_id("Slack_descriptionpost").get_attribute("value"),
                             link_url=driver.find_element_by_id("Slack_linkurlpost").get_attribute("value"),
                             image_url="pas",
                             date_from=datetime_converter("2018-07-01"),
                             date_until=datetime_converter("2018-07-01"), extra=json.dumps(extra))
            db.session.add(pub)
            db.session.commit()
            driver.get('http://127.0.0.1:5000/')
            # wait.until(EC.element_to_be_clickable((By.ID, "moderate_" + str(id_channel))))
            driver.find_element_by_id("moderate_" + str(id_post)).click()
            assert driver.find_element_by_id("titlepost").get_attribute(
                "value") == "Test"
            assert driver.find_element_by_id("descrpost").get_attribute(
                "value") == "Frontend"
            assert driver.find_element_by_id("linkurlpost").get_attribute(
                "value") == "http://127.0.0.1:5000/new"
            driver.close()
            teardown_db(id_channel, id_post)
        except Exception as e:
            driver.close()
            teardown_db(id_channel, id_post)
            assert False, e

    def test_basic_warning(self, client):
        try:
            id_channel, id_post = setup_db()
            driver = webdriver.Firefox()
            driver.get('http://127.0.0.1:5000/')
            wait = WebDriverWait(driver, 10)
            driver.find_element_by_link_text("Login").click()
            driver.find_element_by_name("j_username").click()
            driver.find_element_by_name("j_username").clear()
            driver.find_element_by_name("j_username").send_keys("myself")
            driver.find_element_by_name("j_password").click()
            driver.find_element_by_name("j_password").clear()
            driver.find_element_by_name("j_password").send_keys("myself")
            driver.find_element_by_xpath(
                "(.//*[normalize-space(text()) and normalize-space(.)='Password:'])[1]/following::input[2]").click()
            wait = WebDriverWait(driver, 10)
            wait.until(EC.element_to_be_clickable((By.LINK_TEXT, 'New post')))
            driver.find_element_by_link_text("New post").click()
            driver.find_element_by_id("chan_option_" + str(id_channel)).click()
            driver.find_element_by_id("titlepost").click()
            driver.find_element_by_id("titlepost").clear()
            driver.find_element_by_id("titlepost").send_keys("Test")
            driver.find_element_by_id("descriptionpost").click()
            driver.find_element_by_id("descriptionpost").clear()
            driver.find_element_by_id("descriptionpost").send_keys(
                "Frontend")
            driver.find_element_by_id("linkurlpost").click()
            driver.find_element_by_id("linkurlpost").clear()
            driver.find_element_by_id("linkurlpost").send_keys("http://127.0.0.1:5000/new")
            driver.find_element_by_id("datefrompost").click()
            driver.find_element_by_id("datefrompost").clear()
            driver.find_element_by_id("datefrompost").send_keys("2020-11-21")
            driver.find_element_by_id("dateuntilpost").click()
            driver.find_element_by_id("dateuntilpost").clear()
            driver.find_element_by_id("dateuntilpost").send_keys("2021-01-29")
            driver.find_element_by_link_text("Slack").click()
            extra = {}
            pub = Publishing(post_id=id_post, channel_id=id_channel, state=0,
                             title=driver.find_element_by_id("Slack_titlepost").get_attribute("value"),
                             description=driver.find_element_by_id("Slack_descriptionpost").get_attribute("value"),
                             link_url=driver.find_element_by_id("Slack_linkurlpost").get_attribute("value"),
                             image_url="pas",
                             date_from=datetime_converter("2050-07-01"),
                             date_until=datetime_converter("2050-07-01"), extra=json.dumps(extra))
            db.session.add(pub)
            db.session.commit()
            driver.get('http://127.0.0.1:5000/')
            # wait.until(EC.element_to_be_clickable((By.ID, "moderate_" + str(id_channel))))
            driver.find_element_by_id("moderate_" + str(id_post)).click()
            driver.find_element_by_id("pub-button").click()
            assert driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Moderate this publication'])[1]/following::div[1]").text == "Warning!: Please configure the channel first"
            driver.close()
            teardown_db(id_channel, id_post)
        except Exception as e:
            driver.close()
            teardown_db(id_channel, id_post)
            assert False, e

    def test_basic_warning2(self, client):
        try:
            id_channel, id_post = setup_db()
            driver = webdriver.Firefox()
            driver.get('http://127.0.0.1:5000/')
            wait = WebDriverWait(driver, 10)
            driver.find_element_by_link_text("Login").click()
            driver.find_element_by_name("j_username").click()
            driver.find_element_by_name("j_username").clear()
            driver.find_element_by_name("j_username").send_keys("myself")
            driver.find_element_by_name("j_password").click()
            driver.find_element_by_name("j_password").clear()
            driver.find_element_by_name("j_password").send_keys("myself")
            driver.find_element_by_xpath(
                "(.//*[normalize-space(text()) and normalize-space(.)='Password:'])[1]/following::input[2]").click()
            wait = WebDriverWait(driver, 10)
            wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Channels")))
            driver.find_element_by_link_text("Channels").click()
            driver.find_element_by_link_text("Configure").click()
            driver.find_element_by_id("token").click()
            driver.find_element_by_id("token").clear()
            driver.find_element_by_id("token").send_keys("xoxb-478281424595-487185661847-YVh8O74HfdCtAJj7vuSw9Acv")
            driver.find_element_by_id("channel name").click()
            driver.find_element_by_id("channel name").clear()
            driver.find_element_by_id("channel name").send_keys("major")
            driver.find_element_by_xpath(
                "(.//*[normalize-space(text()) and normalize-space(.)='channel name'])[1]/following::button[1]").click()

            wait = WebDriverWait(driver, 10)
            wait.until(EC.element_to_be_clickable((By.LINK_TEXT, 'New post')))
            driver.find_element_by_link_text("New post").click()
            driver.find_element_by_id("chan_option_" + str(id_channel)).click()
            driver.find_element_by_id("titlepost").click()
            driver.find_element_by_id("titlepost").clear()
            driver.find_element_by_id("titlepost").send_keys("Test")
            driver.find_element_by_id("descriptionpost").click()
            driver.find_element_by_id("descriptionpost").clear()
            driver.find_element_by_id("descriptionpost").send_keys(
                "Frontend")
            driver.find_element_by_id("linkurlpost").click()
            driver.find_element_by_id("linkurlpost").clear()
            driver.find_element_by_id("linkurlpost").send_keys("http://127.0.0.1:5000/new")
            driver.find_element_by_id("datefrompost").click()
            driver.find_element_by_id("datefrompost").clear()
            driver.find_element_by_id("datefrompost").send_keys("2020-11-21")
            driver.find_element_by_id("dateuntilpost").click()
            driver.find_element_by_id("dateuntilpost").clear()
            driver.find_element_by_id("dateuntilpost").send_keys("2021-01-29")
            driver.find_element_by_link_text("Slack").click()
            extra = {}
            pub = Publishing(post_id=id_post, channel_id=id_channel, state=0,
                             title=driver.find_element_by_id("Slack_titlepost").get_attribute("value"),
                             description=driver.find_element_by_id("Slack_descriptionpost").get_attribute("value"),
                             link_url=driver.find_element_by_id("Slack_linkurlpost").get_attribute("value"),
                             image_url="pas",
                             date_from=datetime_converter("2050-07-01"),
                             date_until=datetime_converter("2050-07-01"), extra=json.dumps(extra))
            db.session.add(pub)
            db.session.commit()
            driver.get('http://127.0.0.1:5000/')
            # wait.until(EC.element_to_be_clickable((By.ID, "moderate_" + str(id_channel))))
            driver.find_element_by_id("moderate_" + str(id_post)).click()
            driver.find_element_by_id("pub-button").click()
            assert driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Moderate this publication'])[1]/following::div[1]").text == "Warning!: Channel not found, please review your configuration"
            driver.close()
            teardown_db(id_channel, id_post)
        except Exception as e:
            driver.close()
            teardown_db(id_channel, id_post)
            assert False, e

    def test_basic_publish(self, client):
        try:
            id_channel, id_post = setup_db()
            driver = webdriver.Firefox()
            driver.get('http://127.0.0.1:5000/')
            wait = WebDriverWait(driver, 10)
            driver.find_element_by_link_text("Login").click()
            driver.find_element_by_name("j_username").click()
            driver.find_element_by_name("j_username").clear()
            driver.find_element_by_name("j_username").send_keys("myself")
            driver.find_element_by_name("j_password").click()
            driver.find_element_by_name("j_password").clear()
            driver.find_element_by_name("j_password").send_keys("myself")
            driver.find_element_by_xpath(
                "(.//*[normalize-space(text()) and normalize-space(.)='Password:'])[1]/following::input[2]").click()
            wait = WebDriverWait(driver, 10)
            wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Channels")))
            driver.find_element_by_link_text("Channels").click()
            driver.find_element_by_link_text("Configure").click()
            driver.find_element_by_id("token").click()
            driver.find_element_by_id("token").clear()
            driver.find_element_by_id("token").send_keys("xoxb-478281424595-487185661847-YVh8O74HfdCtAJj7vuSw9Acv")
            driver.find_element_by_id("channel name").click()
            driver.find_element_by_id("channel name").clear()
            driver.find_element_by_id("channel name").send_keys("testing-bot")
            driver.find_element_by_xpath(
                "(.//*[normalize-space(text()) and normalize-space(.)='channel name'])[1]/following::button[1]").click()

            wait = WebDriverWait(driver, 10)
            wait.until(EC.element_to_be_clickable((By.LINK_TEXT, 'New post')))
            driver.find_element_by_link_text("New post").click()
            driver.find_element_by_id("chan_option_" + str(id_channel)).click()
            driver.find_element_by_id("titlepost").click()
            driver.find_element_by_id("titlepost").clear()
            driver.find_element_by_id("titlepost").send_keys("Test")
            driver.find_element_by_id("descriptionpost").click()
            driver.find_element_by_id("descriptionpost").clear()
            driver.find_element_by_id("descriptionpost").send_keys(
                "Frontend")
            driver.find_element_by_id("linkurlpost").click()
            driver.find_element_by_id("linkurlpost").clear()
            driver.find_element_by_id("linkurlpost").send_keys("http://127.0.0.1:5000/new")
            driver.find_element_by_id("datefrompost").click()
            driver.find_element_by_id("datefrompost").clear()
            driver.find_element_by_id("datefrompost").send_keys("2020-11-21")
            driver.find_element_by_id("dateuntilpost").click()
            driver.find_element_by_id("dateuntilpost").clear()
            driver.find_element_by_id("dateuntilpost").send_keys("2021-01-29")
            driver.find_element_by_link_text("Slack").click()
            extra = {}
            pub = Publishing(post_id=id_post, channel_id=id_channel, state=0,
                             title=driver.find_element_by_id("Slack_titlepost").get_attribute("value"),
                             description=driver.find_element_by_id("Slack_descriptionpost").get_attribute("value"),
                             link_url=driver.find_element_by_id("Slack_linkurlpost").get_attribute("value"),
                             image_url="pas",
                             date_from=datetime_converter("2050-07-01"),
                             date_until=datetime_converter("2050-07-01"), extra=json.dumps(extra))
            db.session.add(pub)
            db.session.commit()
            driver.get('http://127.0.0.1:5000/')
            # wait.until(EC.element_to_be_clickable((By.ID, "moderate_" + str(id_channel))))
            driver.find_element_by_id("moderate_" + str(id_post)).click()
            driver.find_element_by_id("pub-button").click()
            assert driver.title == 'Index - Superform', driver.title
            driver.close()
            teardown_db(id_channel, id_post)
        except Exception as e:
            driver.close()
            teardown_db(id_channel, id_post)
            assert False, e
