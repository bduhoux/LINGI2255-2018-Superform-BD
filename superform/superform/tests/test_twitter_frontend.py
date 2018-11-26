from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

import pytest
from selenium import webdriver
from superform import db, create_app
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture
def app():
    app = create_app(True)
    return app


class TestLiveServer:

    def test_basic(self):
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
        driver.find_element_by_id("chan_option_1").click()
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

    def test_two_tweet(self):
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
        driver.find_element_by_id("chan_option_1").click()
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

    def test_link(self):
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
        driver.find_element_by_id("chan_option_1").click()
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

    def test_truncate(self):
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
        driver.find_element_by_id("chan_option_1").click()
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

    def test_characters(self):
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
        driver.find_element_by_id("chan_option_1").click()
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


    def test_moderate(self):
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
        driver.find_element_by_id("chan_option_1").click()
        driver.find_element_by_link_text("Twitter").click()
        driver.find_element_by_id("publish-button").click()
        driver.find_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)='myself'])[6]/following::a[1]").click()
        driver.find_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)='(262 out of 280 characters)'])[1]/following::input[2]").click()
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
        #sleep(5)
        print(driver.find_element_by_id("tweet_1").get_attribute(
            "value"))
        assert driver.find_element_by_id("tweet_1").get_attribute(
            "value") == "[1/2] An duis ubique mei, amet commodo dignissim ne eam, vide velit adipiscing est ad. Has eu inani gloriatur. Ius ea zril malorum aliquid. Et pri deleniti euripidis adversarium. Cum hinc putant laoreet ei, ea ullum tamquam vis, cu quo modus ignota officiis.\n\nEum ea nulla…"
        assert driver.find_element_by_id("tweet_2").get_attribute(
            "value") == "[2/2] exerci, paulo dolore recusabo mel et. Per altera salutatus ad. Cu veri dicat has. Ex erant viris vis, id senserit interesset referrentur nec. Periculis salutatus reformidans eam an, eum te aliquid probatus, no ius corpora petentium. http://127.0.0.1:5000/new"
        assert driver.find_element_by_id("tweet_3").get_attribute(
            "value") == "some random text to test"

        driver.close()

