import datetime
import time

import pytest


@pytest.fixture
def firefox_options(firefox_options, pytestconfig):
    # Don't open the browser during the tests
    firefox_options.add_argument('-headless')
    return firefox_options


@pytest.mark.slow
def test_frontend(selenium):
    # Selenium will poll the DOM for at most 1 second when trying to access
    # an element that's not yet available (maybe loaded via a script)
    selenium.implicitly_wait(1)

    # Login
    selenium.get('http://localhost:5000/login')
    selenium.find_element_by_name('j_username').send_keys('myself')
    selenium.find_element_by_name('j_password').send_keys('myself')
    selenium.find_element_by_css_selector('input[type=submit]').click()

    # Dismiss Firefox's security warning (sending login info to a non-HTTPS page)
    selenium.switch_to.alert.accept()
    # Explicitly wait for the warning to go away, as the implicit wait isn't enough
    time.sleep(0.3)

    # Navigate to the "New Post" page
    selenium.get('http://localhost:5000/new')

    # Check the ICTV channel checkbox
    selenium.find_element_by_css_selector('input[data-module="superform.plugins.ictv"]').click()

    # Post information
    post_title = 'ICTV functional test ' + str(datetime.datetime.now())
    today = datetime.date.today().strftime('%Y-%m-%d')

    # Fill out the main form
    selenium.find_element_by_name('titlepost').send_keys(post_title)
    selenium.find_element_by_name('descriptionpost').send_keys('Test post')
    selenium.find_element_by_name('linkurlpost').send_keys('http://example.com/archival')
    selenium.find_element_by_name('datefrompost').send_keys(today)
    selenium.find_element_by_name('dateuntilpost').send_keys(today)

    # Navigate to the ICTV tab
    selenium.find_element_by_css_selector('.nav-item[data-module="superform.plugins.ictv"]').click()

    # Fill out the ICTV tab
    tab_fields = selenium.find_elements_by_css_selector('fieldset[name=ictv] [type=text]')
    title_field, subtitle_field, desc_field = tab_fields[:3]
    title_field.send_keys('Test title')
    subtitle_field.send_keys('Test subtitle')
    desc_field.send_keys('Test description')

    # Submit
    selenium.find_element_by_id('publish-button').click()

    assert post_title in selenium.find_element_by_tag_name('body').text
