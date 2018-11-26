import pytest
from selenium import webdriver
import os, tempfile
from superform import db, create_app
from flask import url_for
from urllib.request import urlopen

@pytest.fixture
def app():
    app = create_app(True)
    return app

@pytest.mark.usefixtures('live_server')
class TestLiveServer:
    def test_basic(self):
        driver = webdriver.Firefox()
        driver.get(url_for('.index', _external=True))
        driver.find_element_by_link_text("Login").click()
        driver.find_element_by_name("j_username").click()
        driver.find_element_by_name("j_username").clear()
        driver.find_element_by_name("j_username").send_keys("myself")
        driver.find_element_by_name("j_password").click()
        driver.find_element_by_name("j_password").clear()
        driver.find_element_by_name("j_password").send_keys("myself")
        driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Password:'])[1]/following::input[2]").click()
        driver.find_element_by_link_text("Search").click()
        driver.find_element_by_id("search_word").click()
        driver.find_element_by_id("search_word").clear()
        driver.find_element_by_id("search_word").send_keys("test")
        driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Search'])[2]/following::div[4]").click()
        driver.find_element_by_id("submit_search").click()
        assert driver.title == 'Index - Superform', driver.title

