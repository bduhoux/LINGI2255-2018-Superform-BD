import json
import os
import tempfile
from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

import pytest
from selenium import webdriver

from plugins.Twitter import get_channel_fields
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

    def test_basic(self, client):
        setup_db()
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
        driver.find_element_by_id("chan_option_-1").click()
        driver.find_element_by_id("descriptionpost").click()
        driver.find_element_by_id("descriptionpost").click()
        driver.find_element_by_id("descriptionpost").clear()
        driver.find_element_by_id("descriptionpost").send_keys(
            "An duis ubique mei, amet commodo dignissim ne eam, vide velit adipiscing est ad. Has eu inani gloriatur. Ius ea zril malorum aliquid. Et pri deleniti euripidis adversarium. Cum hinc putant laoreet ei, ea ullum tamquam vis, cu quo modus ignota officiis.")
        driver.find_element_by_id("datefrompost").click()
        driver.find_element_by_id("datefrompost").clear()
        driver.find_element_by_id("datefrompost").send_keys("2020-11-21")
        driver.find_element_by_id("dateuntilpost").click()
        driver.find_element_by_id("dateuntilpost").clear()
        driver.find_element_by_id("dateuntilpost").send_keys("2021-01-29")
        driver.find_element_by_link_text("Twitter").click()
        assert driver.find_element_by_id("Twitter_tweet_1").get_attribute(
            "value") == "An duis ubique mei, amet commodo dignissim ne eam, vide velit adipiscing est ad. Has eu inani gloriatur. Ius ea zril malorum aliquid. Et pri deleniti euripidis adversarium. Cum hinc putant laoreet ei, ea ullum tamquam vis, cu quo modus ignota officiis."
        driver.close()
        teardown_db()

    def test_two_tweet(self):
        setup_db()
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
        driver.find_element_by_id("chan_option_-1").click()
        driver.find_element_by_id("descriptionpost").click()
        driver.find_element_by_id("descriptionpost").click()
        driver.find_element_by_id("descriptionpost").clear()
        driver.find_element_by_id("descriptionpost").send_keys(
            "An duis ubique mei, amet commodo dignissim ne eam, vide velit adipiscing est ad. Has eu inani gloriatur. Ius ea zril malorum aliquid. Et pri deleniti euripidis adversarium. Cum hinc putant laoreet ei, ea ullum tamquam vis, cu quo modus ignota officiis.\n\nEum ea nulla exerci, paulo dolore recusabo mel et. Per altera salutatus ad. Cu veri dicat has. Ex erant viris vis, id senserit interesset referrentur nec. Periculis salutatus reformidans eam an, eum te aliquid probatus, no ius corpora petentium.")
        driver.find_element_by_id("datefrompost").click()
        driver.find_element_by_id("datefrompost").clear()
        driver.find_element_by_id("datefrompost").send_keys("2020-11-21")
        driver.find_element_by_id("dateuntilpost").click()
        driver.find_element_by_id("dateuntilpost").clear()
        driver.find_element_by_id("dateuntilpost").send_keys("2021-01-29")
        driver.find_element_by_link_text("Twitter").click()
        assert driver.find_element_by_id("Twitter_tweet_1").get_attribute(
            "value") == "[1/2] An duis ubique mei, amet commodo dignissim ne eam, vide velit adipiscing est ad. Has eu inani gloriatur. Ius ea zril malorum aliquid. Et pri deleniti euripidis adversarium. Cum hinc putant laoreet ei, ea ullum tamquam vis, cu quo modus ignota officiis.\n\nEum ea nulla…"
        assert driver.find_element_by_id("Twitter_tweet_2").get_attribute(
            "value") == "[2/2] exerci, paulo dolore recusabo mel et. Per altera salutatus ad. Cu veri dicat has. Ex erant viris vis, id senserit interesset referrentur nec. Periculis salutatus reformidans eam an, eum te aliquid probatus, no ius corpora petentium."
        driver.close()
        teardown_db()

    def test_link(self):
        setup_db()
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
        driver.find_element_by_id("chan_option_-1").click()
        driver.find_element_by_id("descriptionpost").click()
        driver.find_element_by_id("descriptionpost").click()
        driver.find_element_by_id("descriptionpost").clear()
        driver.find_element_by_id("descriptionpost").send_keys(
            "An duis ubique mei, amet commodo dignissim ne eam, vide velit adipiscing est ad. Has eu inani gloriatur. Ius ea zril malorum aliquid. Et pri deleniti euripidis adversarium. Cum hinc putant laoreet ei, ea ullum tamquam vis, cu quo modus ignota officiis.\n\nEum ea nulla exerci, paulo dolore recusabo mel et. Per altera salutatus ad. Cu veri dicat has. Ex erant viris vis, id senserit interesset referrentur nec. Periculis salutatus reformidans eam an, eum te aliquid probatus, no ius corpora petentium.")
        driver.find_element_by_id("linkurlpost").click()
        driver.find_element_by_id("linkurlpost").clear()
        driver.find_element_by_id("linkurlpost").send_keys("http://127.0.0.1:5000/new")
        driver.find_element_by_id("datefrompost").click()
        driver.find_element_by_id("datefrompost").clear()
        driver.find_element_by_id("datefrompost").send_keys("2020-11-21")
        driver.find_element_by_id("dateuntilpost").click()
        driver.find_element_by_id("dateuntilpost").clear()
        driver.find_element_by_id("dateuntilpost").send_keys("2021-01-29")
        driver.find_element_by_link_text("Twitter").click()
        assert driver.find_element_by_id("Twitter_tweet_1").get_attribute(
            "value") == "[1/2] An duis ubique mei, amet commodo dignissim ne eam, vide velit adipiscing est ad. Has eu inani gloriatur. Ius ea zril malorum aliquid. Et pri deleniti euripidis adversarium. Cum hinc putant laoreet ei, ea ullum tamquam vis, cu quo modus ignota officiis.\n\nEum ea nulla…"
        assert driver.find_element_by_id("Twitter_tweet_2").get_attribute(
            "value") == "[2/2] exerci, paulo dolore recusabo mel et. Per altera salutatus ad. Cu veri dicat has. Ex erant viris vis, id senserit interesset referrentur nec. Periculis salutatus reformidans eam an, eum te aliquid probatus, no ius corpora petentium. http://127.0.0.1:5000/new"
        driver.close()
        teardown_db()

    def test_truncate(self):
        setup_db()
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
        driver.find_element_by_id("chan_option_-1").click()
        driver.find_element_by_id("descriptionpost").click()
        driver.find_element_by_id("descriptionpost").click()
        driver.find_element_by_id("descriptionpost").clear()
        driver.find_element_by_id("descriptionpost").send_keys(
            "An duis ubique mei, amet commodo dignissim ne eam, vide velit adipiscing est ad. Has eu inani gloriatur. Ius ea zril malorum aliquid. Et pri deleniti euripidis adversarium. Cum hinc putant laoreet ei, ea ullum tamquam vis, cu quo modus ignota officiis.\n\nEum ea nulla exerci, paulo dolore recusabo mel et. Per altera salutatus ad. Cu veri dicat has. Ex erant viris vis, id senserit interesset referrentur nec. Periculis salutatus reformidans eam an, eum te aliquid probatus, no ius corpora petentium.")
        driver.find_element_by_id("linkurlpost").click()
        driver.find_element_by_id("linkurlpost").clear()
        driver.find_element_by_id("linkurlpost").send_keys("http://127.0.0.1:5000/new")
        driver.find_element_by_id("datefrompost").click()
        driver.find_element_by_id("datefrompost").clear()
        driver.find_element_by_id("datefrompost").send_keys("2020-11-21")
        driver.find_element_by_id("dateuntilpost").click()
        driver.find_element_by_id("dateuntilpost").clear()
        driver.find_element_by_id("dateuntilpost").send_keys("2021-01-29")
        driver.find_element_by_link_text("Twitter").click()
        driver.find_element_by_id("Twitter_truncate").click()
        assert driver.find_element_by_id("Twitter_tweet_1").get_attribute(
            "value") == "An duis ubique mei, amet commodo dignissim ne eam, vide velit adipiscing est ad. Has eu inani gloriatur. Ius ea zril malorum aliquid. Et pri deleniti euripidis adversarium. Cum hinc putant laoreet ei, ea ullum tamquam vis, cu quo modus ignota […] http://127.0.0.1:5000/new"
        driver.close()
        teardown_db()

    def test_characters(self):
        setup_db()
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
        driver.find_element_by_id("chan_option_-1").click()
        driver.find_element_by_id("descriptionpost").click()
        driver.find_element_by_id("descriptionpost").click()
        driver.find_element_by_id("descriptionpost").clear()
        driver.find_element_by_id("descriptionpost").send_keys(
            "An duis ubique mei, amet commodo dignissim ne eam, vide velit adipiscing est ad. Has eu inani gloriatur. Ius ea zril malorum aliquid. Et pri deleniti euripidis adversarium. Cum hinc putant laoreet ei, ea ullum tamquam vis, cu quo modus ignota officiis.\n\nEum ea nulla exerci, paulo dolore recusabo mel et. Per altera salutatus ad. Cu veri dicat has. Ex erant viris vis, id senserit interesset referrentur nec. Periculis salutatus reformidans eam an, eum te aliquid probatus, no ius corpora petentium.")
        driver.find_element_by_id("linkurlpost").click()
        driver.find_element_by_id("linkurlpost").clear()
        driver.find_element_by_id("linkurlpost").send_keys("http://127.0.0.1:5000/new")
        driver.find_element_by_id("datefrompost").click()
        driver.find_element_by_id("datefrompost").clear()
        driver.find_element_by_id("datefrompost").send_keys("2020-11-21")
        driver.find_element_by_id("dateuntilpost").click()
        driver.find_element_by_id("dateuntilpost").clear()
        driver.find_element_by_id("dateuntilpost").send_keys("2021-01-29")
        driver.find_element_by_link_text("Twitter").click()
        assert driver.find_element_by_id("NumberCharacters_1").text == "(274 out of 280 characters)"
        assert driver.find_element_by_id("NumberCharacters_2").text == "(262 out of 280 characters)"
        driver.close()
        teardown_db()

    def test_moderate(self):
        setup_db()
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
        wait.until(EC.element_to_be_clickable((By.ID, 'moderate_-1')))
        driver.find_element_by_link_text("moderate").click()
        driver.find_element_by_id("descriptionpost").click()
        driver.find_element_by_id("descriptionpost").clear()
        driver.find_element_by_id("descriptionpost").send_keys(
            "An duis ubique mei, amet commodo dignissim ne eam, vide velit adipiscing est ad. Has eu inani gloriatur. Ius ea zril malorum aliquid. Et pri deleniti euripidis adversarium. Cum hinc putant laoreet ei, ea ullum tamquam vis, cu quo modus ignota officiis.\\n\\nEum ea nulla exerci, paulo dolore recusabo mel et. Per altera salutatus ad. Cu veri dicat has. Ex erant viris vis, id senserit interesset referrentur nec. Periculis salutatus reformidans eam an, eum te aliquid probatus, no ius corpora petentium.")
        driver.find_element_by_id("linkurlpost").click()
        driver.find_element_by_id("linkurlpost").clear()
        driver.find_element_by_id("linkurlpost").send_keys("http://127.0.0.1:5000/new")
        driver.find_element_by_id("datefrompost").click()
        driver.find_element_by_id("datefrompost").clear()
        driver.find_element_by_id("datefrompost").send_keys("2020-01-25")
        driver.find_element_by_id("dateuntilpost").click()
        driver.find_element_by_id("dateuntilpost").clear()
        driver.find_element_by_id("dateuntilpost").send_keys("2021-01-20")
        driver.find_element_by_id("chan_option_-1").click()
        driver.find_element_by_link_text("Twitter").click()

        extra = get_channel_fields({'Twitter_tweet_1': driver.find_element_by_id("Twitter_tweet_1").get_attribute(
            "value"), 'Twitter_tweet_2': driver.find_element_by_id("Twitter_tweet_2").get_attribute(
            "value")}, 'Twitter')

        pub = Publishing(post_id=-1, channel_id=-1, state=0, title="",
                         description="That know ask case sex ham dear her spot. Weddings followed the all marianne nor whatever settling. Perhaps six prudent several her had offence. Did had way law dinner square tastes. Recommend concealed yet her procuring see consulted depending. Adieus hunted end plenty are his she afraid. Resources agreement contained propriety applauded neglected use yet. ",
                         link_url="http://facebook.com/", image_url="pas", date_from=datetime_converter("2018-07-01"),
                         date_until=datetime_converter("2018-07-01"), extra=json.dumps(extra))
        db.session.add(pub)
        db.session.commit()
        driver.find_element_by_link_text("Home").click()
        driver.find_element_by_id("moderate_-1").click()
        driver.find_element_by_id("tweet_3").click()
        driver.find_element_by_id("tweet_3").clear()
        driver.find_element_by_id("tweet_3").send_keys("some random text to test")
        driver.find_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)='(24 out of 280 characters)'])[1]/following::input[2]").click()
        driver.find_element_by_id("tweet_4").click()
        driver.find_element_by_id("tweet_4").clear()
        driver.find_element_by_id("tweet_4").send_keys("uiocfzuo")
        driver.find_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)='Moderate this publication'])[1]/following::div[2]").click()
        driver.find_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)='(8 out of 280 characters)'])[1]/following::input[1]").click()
        # sleep(5)
        print(driver.find_element_by_id("tweet_1").get_attribute(
            "value"))
        assert driver.find_element_by_id("tweet_1").get_attribute(
            "value") == "[1/2] An duis ubique mei, amet commodo dignissim ne eam, vide velit adipiscing est ad. Has eu inani gloriatur. Ius ea zril malorum aliquid. Et pri deleniti euripidis adversarium. Cum hinc putant laoreet ei, ea ullum tamquam vis, cu quo modus ignota officiis.\n\nEum ea nulla…"
        assert driver.find_element_by_id("tweet_2").get_attribute(
            "value") == "[2/2] exerci, paulo dolore recusabo mel et. Per altera salutatus ad. Cu veri dicat has. Ex erant viris vis, id senserit interesset referrentur nec. Periculis salutatus reformidans eam an, eum te aliquid probatus, no ius corpora petentium. http://127.0.0.1:5000/new"
        assert driver.find_element_by_id("tweet_3").get_attribute(
            "value") == "some random text to test"

        driver.close()
        teardown_db()
