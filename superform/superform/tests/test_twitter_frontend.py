import json
import os

import tempfile

from sqlalchemy.exc import InvalidRequestError

from superform.models import Publishing
from superform.utils import datetime_converter

import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import pytest
from selenium import webdriver
from superform.plugins.Twitter import get_channel_fields
from superform import db, app
from selenium.webdriver.support import expected_conditions as EC

json_data = open(os.path.dirname(os.path.abspath(__file__)) + '/../config.json')
data = json.load(json_data)

channelName = "Twitter_test"
pluginName = "superform.plugins.Twitter"
fieldTested = ["description", "link"]
configuration = {"Access token": data["TWITTER_TEST_ACESS TOKEN"],
                 "Access token secret": data["TWITTER_TEST_ACESS TOKEN_SECRET"]}


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


@pytest.mark.frontEnd
def test_basic(client):
    pytest.helpers.plugin.test_basic(client, channelName, pluginName, fieldTested)


@pytest.mark.frontEnd
def test_basic_moderate(client):
    pytest.helpers.plugin.test_basic_moderate(client, channelName, pluginName, fieldTested)


@pytest.mark.frontEnd
def test_basic_warning(client):
    pytest.helpers.plugin.test_basic_warning(client, channelName, pluginName)


@pytest.mark.frontEnd
def test_basic_publish(client):
    pytest.helpers.plugin.test_basic_publish(client, channelName, pluginName, configuration,
                                             {"tweet_list": [["1", ""]]})


@pytest.mark.frontEnd
def test_basic_preview(client):
    id_channel, id_post = pytest.helpers.plugin.setup_db(channelName, "superform.plugins.Twitter")
    driver = webdriver.Firefox()
    try:
        driver.get('http://localhost:5000/')
        wait = WebDriverWait(driver, 20)
        driver.find_element_by_link_text("Login").click()
        wait.until(EC.element_to_be_clickable((By.NAME, "j_username")))
        driver.find_element_by_name("j_username").click()
        driver.find_element_by_name("j_username").clear()
        driver.find_element_by_name("j_username").send_keys("myself")
        driver.find_element_by_name("j_password").click()
        driver.find_element_by_name("j_password").clear()
        driver.find_element_by_name("j_password").send_keys("myself")
        driver.find_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)='Password:'])[1]/following::input[2]").click()
        driver.switch_to.alert.accept()
        wait = WebDriverWait(driver, 10)
        wait.until(EC.element_to_be_clickable((By.LINK_TEXT, 'New post')))
        driver.find_element_by_link_text("New post").click()
        driver.find_element_by_id("chan_option_" + str(id_channel)).click()
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
        driver.find_element_by_link_text(channelName).click()
        assert driver.find_element_by_id(channelName + "_tweet_1").get_attribute(
            "value") == "An duis ubique mei, amet commodo dignissim ne eam, vide velit adipiscing est ad. Has eu inani gloriatur. Ius ea zril malorum aliquid. Et pri deleniti euripidis adversarium. Cum hinc putant laoreet ei, ea ullum tamquam vis, cu quo modus ignota officiis."
    except AssertionError as e:
        pytest.helpers.plugin.teardown_db(id_channel, id_post)
        driver.close()
        assert False, str(e)
    except InvalidRequestError as e:
        pytest.helpers.plugin.teardown_db(id_channel, id_post)
        driver.close()
        assert False, "An error occurred while testing: {}".format(str(e))
    pytest.helpers.plugin.teardown_db(id_channel, id_post)
    driver.close()


@pytest.mark.frontEnd
def test_two_tweet(client):
    id_channel, id_post = pytest.helpers.plugin.setup_db(channelName, "superform.plugins.Twitter")
    driver = webdriver.Firefox()
    try:
        driver.get('http://localhost:5000/')
        wait = WebDriverWait(driver, 20)
        driver.find_element_by_link_text("Login").click()
        wait.until(EC.element_to_be_clickable((By.NAME, "j_username")))
        driver.find_element_by_name("j_username").click()
        driver.find_element_by_name("j_username").clear()
        driver.find_element_by_name("j_username").send_keys("myself")
        driver.find_element_by_name("j_password").click()
        driver.find_element_by_name("j_password").clear()
        driver.find_element_by_name("j_password").send_keys("myself")
        driver.find_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)='Password:'])[1]/following::input[2]").click()
        driver.switch_to.alert.accept()
        wait = WebDriverWait(driver, 10)
        wait.until(EC.element_to_be_clickable((By.LINK_TEXT, 'New post')))
        driver.find_element_by_link_text("New post").click()
        driver.find_element_by_id("chan_option_" + str(id_channel)).click()
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
        driver.find_element_by_link_text(channelName).click()
        assert driver.find_element_by_id(channelName + "_tweet_1").get_attribute(
            "value") == "[1/2] An duis ubique mei, amet commodo dignissim ne eam, vide velit adipiscing est ad. Has eu inani gloriatur. Ius ea zril malorum aliquid. Et pri deleniti euripidis adversarium. Cum hinc putant laoreet ei, ea ullum tamquam vis, cu quo modus ignota officiis.\n\nEum ea nulla…"
        assert driver.find_element_by_id(channelName + "_tweet_2").get_attribute(
            "value") == "[2/2] exerci, paulo dolore recusabo mel et. Per altera salutatus ad. Cu veri dicat has. Ex erant viris vis, id senserit interesset referrentur nec. Periculis salutatus reformidans eam an, eum te aliquid probatus, no ius corpora petentium."
    except AssertionError as e:
        pytest.helpers.plugin.teardown_db(id_channel, id_post)
        driver.close()
        assert False, str(e)
    except InvalidRequestError as e:
        pytest.helpers.plugin.teardown_db(id_channel, id_post)
        driver.close()
        assert False, "An error occurred while testing: {}".format(str(e))
    pytest.helpers.plugin.teardown_db(id_channel, id_post)
    driver.close()


@pytest.mark.frontEnd
def test_link(client):
    id_channel, id_post = pytest.helpers.plugin.setup_db(channelName, "superform.plugins.Twitter")
    driver = webdriver.Firefox()
    try:
        driver.get('http://localhost:5000/')
        wait = WebDriverWait(driver, 20)
        driver.find_element_by_link_text("Login").click()
        wait.until(EC.element_to_be_clickable((By.NAME, "j_username")))
        driver.find_element_by_name("j_username").click()
        driver.find_element_by_name("j_username").clear()
        driver.find_element_by_name("j_username").send_keys("myself")
        driver.find_element_by_name("j_password").click()
        driver.find_element_by_name("j_password").clear()
        driver.find_element_by_name("j_password").send_keys("myself")
        driver.find_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)='Password:'])[1]/following::input[2]").click()
        driver.switch_to.alert.accept()
        wait = WebDriverWait(driver, 10)
        wait.until(EC.element_to_be_clickable((By.LINK_TEXT, 'New post')))
        driver.find_element_by_link_text("New post").click()
        driver.find_element_by_id("chan_option_" + str(id_channel)).click()
        driver.find_element_by_id("descriptionpost").click()
        driver.find_element_by_id("descriptionpost").click()
        driver.find_element_by_id("descriptionpost").clear()
        driver.find_element_by_id("descriptionpost").send_keys(
            "An duis ubique mei, amet commodo dignissim ne eam, vide velit adipiscing est ad. Has eu inani gloriatur. Ius ea zril malorum aliquid. Et pri deleniti euripidis adversarium. Cum hinc putant laoreet ei, ea ullum tamquam vis, cu quo modus ignota officiis.\n\nEum ea nulla exerci, paulo dolore recusabo mel et. Per altera salutatus ad. Cu veri dicat has. Ex erant viris vis, id senserit interesset referrentur nec. Periculis salutatus reformidans eam an, eum te aliquid probatus, no ius corpora petentium.")
        driver.find_element_by_id("linkurlpost").click()
        driver.find_element_by_id("linkurlpost").clear()
        driver.find_element_by_id("linkurlpost").send_keys("http://localhost:5000/new")
        driver.find_element_by_id("datefrompost").click()
        driver.find_element_by_id("datefrompost").clear()
        driver.find_element_by_id("datefrompost").send_keys("2020-11-21")
        driver.find_element_by_id("dateuntilpost").click()
        driver.find_element_by_id("dateuntilpost").clear()
        driver.find_element_by_id("dateuntilpost").send_keys("2021-01-29")
        driver.find_element_by_link_text(channelName).click()
        assert driver.find_element_by_id(channelName + "_tweet_1").get_attribute(
            "value") == "[1/2] An duis ubique mei, amet commodo dignissim ne eam, vide velit adipiscing est ad. Has eu inani gloriatur. Ius ea zril malorum aliquid. Et pri deleniti euripidis adversarium. Cum hinc putant laoreet ei, ea ullum tamquam vis, cu quo modus ignota officiis.\n\nEum ea nulla…"
        assert driver.find_element_by_id(channelName + "_tweet_2").get_attribute(
            "value") == "[2/2] exerci, paulo dolore recusabo mel et. Per altera salutatus ad. Cu veri dicat has. Ex erant viris vis, id senserit interesset referrentur nec. Periculis salutatus reformidans eam an, eum te aliquid probatus, no ius corpora petentium. http://localhost:5000/new"
    except AssertionError as e:
        pytest.helpers.plugin.teardown_db(id_channel, id_post)
        driver.close()
        assert False, str(e)
    except InvalidRequestError as e:
        pytest.helpers.plugin.teardown_db(id_channel, id_post)
        driver.close()
        assert False, "An error occurred while testing: {}".format(str(e))
    pytest.helpers.plugin.teardown_db(id_channel, id_post)
    driver.close()


@pytest.mark.frontEnd
def test_truncate(client):
    id_channel, id_post = pytest.helpers.plugin.setup_db(channelName, "superform.plugins.Twitter")
    driver = webdriver.Firefox()
    try:
        driver.get('http://localhost:5000/')
        wait = WebDriverWait(driver, 20)
        driver.find_element_by_link_text("Login").click()
        wait.until(EC.element_to_be_clickable((By.NAME, "j_username")))
        driver.find_element_by_name("j_username").click()
        driver.find_element_by_name("j_username").clear()
        driver.find_element_by_name("j_username").send_keys("myself")
        driver.find_element_by_name("j_password").click()
        driver.find_element_by_name("j_password").clear()
        driver.find_element_by_name("j_password").send_keys("myself")
        driver.find_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)='Password:'])[1]/following::input[2]").click()
        driver.switch_to.alert.accept()
        wait = WebDriverWait(driver, 10)
        wait.until(EC.element_to_be_clickable((By.LINK_TEXT, 'New post')))
        driver.find_element_by_link_text("New post").click()
        driver.find_element_by_id("chan_option_" + str(id_channel)).click()
        driver.find_element_by_id("descriptionpost").click()
        driver.find_element_by_id("descriptionpost").click()
        driver.find_element_by_id("descriptionpost").clear()
        driver.find_element_by_id("descriptionpost").send_keys(
            "An duis ubique mei, amet commodo dignissim ne eam, vide velit adipiscing est ad. Has eu inani gloriatur. Ius ea zril malorum aliquid. Et pri deleniti euripidis adversarium. Cum hinc putant laoreet ei, ea ullum tamquam vis, cu quo modus ignota officiis.\n\nEum ea nulla exerci, paulo dolore recusabo mel et. Per altera salutatus ad. Cu veri dicat has. Ex erant viris vis, id senserit interesset referrentur nec. Periculis salutatus reformidans eam an, eum te aliquid probatus, no ius corpora petentium.")
        driver.find_element_by_id("linkurlpost").click()
        driver.find_element_by_id("linkurlpost").clear()
        driver.find_element_by_id("linkurlpost").send_keys("http://localhost:5000/new")
        driver.find_element_by_id("datefrompost").click()
        driver.find_element_by_id("datefrompost").clear()
        driver.find_element_by_id("datefrompost").send_keys("2020-11-21")
        driver.find_element_by_id("dateuntilpost").click()
        driver.find_element_by_id("dateuntilpost").clear()
        driver.find_element_by_id("dateuntilpost").send_keys("2021-01-29")
        driver.find_element_by_link_text(channelName).click()
        driver.find_element_by_id(channelName + "_truncate").click()
        assert driver.find_element_by_id(channelName + "_tweet_1").get_attribute(
            "value") == "An duis ubique mei, amet commodo dignissim ne eam, vide velit adipiscing est ad. Has eu inani gloriatur. Ius ea zril malorum aliquid. Et pri deleniti euripidis adversarium. Cum hinc putant laoreet ei, ea ullum tamquam vis, cu quo modus ignota […] http://localhost:5000/new"
    except AssertionError as e:
        pytest.helpers.plugin.teardown_db(id_channel, id_post)
        driver.close()
        assert False, str(e)
    except InvalidRequestError as e:
        pytest.helpers.plugin.teardown_db(id_channel, id_post)
        driver.close()
        assert False, "An error occurred while testing: {}".format(str(e))
    pytest.helpers.plugin.teardown_db(id_channel, id_post)
    driver.close()


@pytest.mark.frontEnd
def test_characters(client):
    id_channel, id_post = pytest.helpers.plugin.setup_db(channelName, "superform.plugins.Twitter")
    driver = webdriver.Firefox()
    try:
        driver.get('http://localhost:5000/')
        wait = WebDriverWait(driver, 20)
        driver.find_element_by_link_text("Login").click()
        wait.until(EC.element_to_be_clickable((By.NAME, "j_username")))
        driver.find_element_by_name("j_username").click()
        driver.find_element_by_name("j_username").clear()
        driver.find_element_by_name("j_username").send_keys("myself")
        driver.find_element_by_name("j_password").click()
        driver.find_element_by_name("j_password").clear()
        driver.find_element_by_name("j_password").send_keys("myself")
        driver.find_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)='Password:'])[1]/following::input[2]").click()
        driver.switch_to.alert.accept()
        wait = WebDriverWait(driver, 10)
        wait.until(EC.element_to_be_clickable((By.LINK_TEXT, 'New post')))
        driver.find_element_by_link_text("New post").click()
        driver.find_element_by_id("chan_option_" + str(id_channel)).click()
        driver.find_element_by_id("descriptionpost").click()
        driver.find_element_by_id("descriptionpost").click()
        driver.find_element_by_id("descriptionpost").clear()
        driver.find_element_by_id("descriptionpost").send_keys(
            "An duis ubique mei, amet commodo dignissim ne eam, vide velit adipiscing est ad. Has eu inani gloriatur. Ius ea zril malorum aliquid. Et pri deleniti euripidis adversarium. Cum hinc putant laoreet ei, ea ullum tamquam vis, cu quo modus ignota officiis.\n\nEum ea nulla exerci, paulo dolore recusabo mel et. Per altera salutatus ad. Cu veri dicat has. Ex erant viris vis, id senserit interesset referrentur nec. Periculis salutatus reformidans eam an, eum te aliquid probatus, no ius corpora petentium.")
        driver.find_element_by_id("linkurlpost").click()
        driver.find_element_by_id("linkurlpost").clear()
        driver.find_element_by_id("linkurlpost").send_keys("http://localhost:5000/new")
        driver.find_element_by_id("datefrompost").click()
        driver.find_element_by_id("datefrompost").clear()
        driver.find_element_by_id("datefrompost").send_keys("2020-11-21")
        driver.find_element_by_id("dateuntilpost").click()
        driver.find_element_by_id("dateuntilpost").clear()
        driver.find_element_by_id("dateuntilpost").send_keys("2021-01-29")
        driver.find_element_by_link_text(channelName).click()
        assert driver.find_element_by_id("NumberCharacters_1").text == "(274 out of 280 characters)"
        assert driver.find_element_by_id("NumberCharacters_2").text == "(264 out of 280 characters)"
        assert driver.find_element_by_id("status_too_many_chars").get_attribute(
            'innerHTML') == " Too many characters for one tweet! "
    except AssertionError as e:
        pytest.helpers.plugin.teardown_db(id_channel, id_post)
        driver.close()
        assert False, str(e)
    except InvalidRequestError as e:
        pytest.helpers.plugin.teardown_db(id_channel, id_post)
        driver.close()
        assert False, "An error occurred while testing: {}".format(str(e))
    pytest.helpers.plugin.teardown_db(id_channel, id_post)
    driver.close()


@pytest.mark.frontEnd
def test_moderate(client):
    id_channel, id_post = pytest.helpers.plugin.setup_db(channelName, "superform.plugins.Twitter")
    driver = webdriver.Firefox()
    try:
        driver.get('http://localhost:5000/')
        wait = WebDriverWait(driver, 20)
        driver.find_element_by_link_text("Login").click()
        wait.until(EC.element_to_be_clickable((By.NAME, "j_username")))
        driver.find_element_by_name("j_username").click()
        driver.find_element_by_name("j_username").clear()
        driver.find_element_by_name("j_username").send_keys("myself")
        driver.find_element_by_name("j_password").click()
        driver.find_element_by_name("j_password").clear()
        driver.find_element_by_name("j_password").send_keys("myself")
        driver.find_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)='Password:'])[1]/following::input[2]").click()
        driver.switch_to.alert.accept()
        wait = WebDriverWait(driver, 10)
        wait.until(EC.element_to_be_clickable((By.LINK_TEXT, 'New post')))
        driver.find_element_by_link_text("New post").click()
        driver.find_element_by_id("chan_option_" + str(id_channel)).click()
        driver.find_element_by_id("descriptionpost").click()
        driver.find_element_by_id("descriptionpost").click()
        driver.find_element_by_id("descriptionpost").clear()
        driver.find_element_by_id("descriptionpost").send_keys(
            "An duis ubique mei, amet commodo dignissim ne eam, vide velit adipiscing est ad. Has eu inani gloriatur. Ius ea zril malorum aliquid. Et pri deleniti euripidis adversarium. Cum hinc putant laoreet ei, ea ullum tamquam vis, cu quo modus ignota officiis.\n\nEum ea nulla exerci, paulo dolore recusabo mel et. Per altera salutatus ad. Cu veri dicat has. Ex erant viris vis, id senserit interesset referrentur nec. Periculis salutatus reformidans eam an, eum te aliquid probatus, no ius corpora petentium.")
        driver.find_element_by_id("linkurlpost").click()
        driver.find_element_by_id("linkurlpost").clear()
        driver.find_element_by_id("linkurlpost").send_keys("http://localhost:5000/new")
        driver.find_element_by_id("datefrompost").click()
        driver.find_element_by_id("datefrompost").clear()
        driver.find_element_by_id("datefrompost").send_keys("2020-11-21")
        driver.find_element_by_id("dateuntilpost").click()
        driver.find_element_by_id("dateuntilpost").clear()
        driver.find_element_by_id("dateuntilpost").send_keys("2021-01-29")
        driver.find_element_by_link_text(channelName).click()
        extra = get_channel_fields(
            {'Twitter_test_tweet_1': driver.find_element_by_id(channelName + "_tweet_1").get_attribute(
                "value"), 'Twitter_test_tweet_2': driver.find_element_by_id(channelName + "_tweet_2").get_attribute(
                "value")}, 'Twitter_test')
        pub = Publishing(post_id=id_post, channel_id=id_channel, state=0, title="",
                         description="That know ask case sex ham dear her spot. Weddings followed the all marianne nor whatever settling. Perhaps six prudent several her had offence. Did had way law dinner square tastes. Recommend concealed yet her procuring see consulted depending. Adieus hunted end plenty are his she afraid. Resources agreement contained propriety applauded neglected use yet. ",
                         link_url="http://localhost:5000/new", image_url="pas",
                         date_from=datetime_converter("2018-07-01"),
                         date_until=datetime_converter("2018-07-01"), extra=json.dumps(extra))
        db.session.add(pub)
        db.session.commit()
        driver.get('http://localhost:5000/')
        # wait.until(EC.element_to_be_clickable((By.ID, "moderate_" + str(id_channel))))
        driver.find_element_by_id("moderate_" + str(id_post)).click()
        driver.find_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)='(264 out of 280 characters)'])[1]/following::input[2]").click()
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
            "value") == "[2/2] exerci, paulo dolore recusabo mel et. Per altera salutatus ad. Cu veri dicat has. Ex erant viris vis, id senserit interesset referrentur nec. Periculis salutatus reformidans eam an, eum te aliquid probatus, no ius corpora petentium. http://localhost:5000/new"
        assert driver.find_element_by_id("tweet_3").get_attribute(
            "value") == "some random text to test"
        try:
            driver.find_element_by_id(channelName + "_tweet_4")
            assert False
        except selenium.common.exceptions.NoSuchElementException:
            assert True
    except AssertionError as e:
        pytest.helpers.plugin.teardown_db(id_channel, id_post)
        driver.close()
        assert False, str(e)
    except InvalidRequestError as e:
        pytest.helpers.plugin.teardown_db(id_channel, id_post)
        driver.close()
        assert False, "An error occurred while testing: {}".format(str(e))
    pytest.helpers.plugin.teardown_db(id_channel, id_post)
    driver.close()


@pytest.mark.frontEnd
def test_add_remove(client):
    id_channel, id_post = pytest.helpers.plugin.setup_db(channelName, "superform.plugins.Twitter")
    driver = webdriver.Firefox()
    try:
        driver.get('http://localhost:5000/')
        wait = WebDriverWait(driver, 20)
        driver.find_element_by_link_text("Login").click()
        wait.until(EC.element_to_be_clickable((By.NAME, "j_username")))
        driver.find_element_by_name("j_username").click()
        driver.find_element_by_name("j_username").clear()
        driver.find_element_by_name("j_username").send_keys("myself")
        driver.find_element_by_name("j_password").click()
        driver.find_element_by_name("j_password").clear()
        driver.find_element_by_name("j_password").send_keys("myself")
        driver.find_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)='Password:'])[1]/following::input[2]").click()
        driver.switch_to.alert.accept()
        wait = WebDriverWait(driver, 10)
        wait.until(EC.element_to_be_clickable((By.LINK_TEXT, 'New post')))
        driver.find_element_by_link_text("New post").click()
        driver.find_element_by_id("descriptionpost").click()
        driver.find_element_by_id("descriptionpost").clear()
        driver.find_element_by_id("descriptionpost").send_keys(
            "An duis ubique mei, amet commodo dignissim ne eam, vide velit adipiscing est ad. Has eu inani gloriatur. Ius ea zril malorum aliquid. Et pri deleniti euripidis adversarium. Cum hinc putant laoreet ei, ea ullum tamquam vis, cu quo modus ignota officiis.\n\nEum ea nulla exerci, paulo dolore recusabo mel et. Per altera salutatus ad. Cu veri dicat has. Ex erant viris vis, id senserit interesset referrentur nec. Periculis salutatus reformidans eam an, eum te aliquid probatus, no ius corpora petentium.")
        driver.find_element_by_id("linkurlpost").click()
        driver.find_element_by_id("linkurlpost").clear()
        driver.find_element_by_id("linkurlpost").send_keys("http://localhost:5000/new")
        driver.find_element_by_id("datefrompost").click()
        driver.find_element_by_id("datefrompost").clear()
        driver.find_element_by_id("datefrompost").send_keys("2020-11-21")
        driver.find_element_by_id("dateuntilpost").click()
        driver.find_element_by_id("dateuntilpost").clear()
        driver.find_element_by_id("dateuntilpost").send_keys("2021-01-29")
        driver.find_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)='Publish'])[1]/following::div[1]").click()
        driver.find_element_by_id("chan_option_" + str(id_channel)).click()
        driver.find_element_by_link_text(channelName).click()
        driver.find_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)='(264 out of 280 characters)'])[1]/following::input[2]").click()
        driver.find_element_by_id(channelName + "_tweet_3").click()
        driver.find_element_by_id(channelName + "_tweet_3").clear()
        driver.find_element_by_id(channelName + "_tweet_3").send_keys("some random text")
        driver.find_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)='(16 out of 280 characters)'])[1]/following::input[2]").click()
        driver.find_element_by_id(channelName + "_tweet_4").click()
        driver.find_element_by_id(channelName + "_tweet_4").clear()
        driver.find_element_by_id(channelName + "_tweet_4").send_keys("sfgethet fdb")
        driver.find_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)='(12 out of 280 characters)'])[1]/following::div[1]").click()
        driver.find_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)='(12 out of 280 characters)'])[1]/following::input[1]").click()
        assert driver.find_element_by_id(channelName + "_tweet_1").get_attribute(
            "value") == "[1/2] An duis ubique mei, amet commodo dignissim ne eam, vide velit adipiscing est ad. Has eu inani gloriatur. Ius ea zril malorum aliquid. Et pri deleniti euripidis adversarium. Cum hinc putant laoreet ei, ea ullum tamquam vis, cu quo modus ignota officiis.\n\nEum ea nulla…"
        assert driver.find_element_by_id(channelName + "_tweet_2").get_attribute(
            "value") == "[2/2] exerci, paulo dolore recusabo mel et. Per altera salutatus ad. Cu veri dicat has. Ex erant viris vis, id senserit interesset referrentur nec. Periculis salutatus reformidans eam an, eum te aliquid probatus, no ius corpora petentium. http://localhost:5000/new"
        assert driver.find_element_by_id(channelName + "_tweet_3").get_attribute(
            "value") == "some random text"
        try:
            driver.find_element_by_id(channelName + "_tweet_4")
            assert False
        except selenium.common.exceptions.NoSuchElementException:
            assert True
    except AssertionError as e:
        pytest.helpers.plugin.teardown_db(id_channel, id_post)
        driver.close()
        assert False, str(e)
    except InvalidRequestError as e:
        pytest.helpers.plugin.teardown_db(id_channel, id_post)
        driver.close()
        assert False, "An error occurred while testing: {}".format(str(e))
    pytest.helpers.plugin.teardown_db(id_channel, id_post)
    driver.close()
