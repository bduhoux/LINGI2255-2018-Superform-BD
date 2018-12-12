import datetime
import time
import json
import os
import urllib.request
import pytest
from superform.plugins import ictv
from superform import app
from superform.models import Publishing
from superform.utils import get_module_full_name


@pytest.fixture
def firefox_options(firefox_options, pytestconfig):
    # Don't open the browser during the tests
    #firefox_options.add_argument('-headless')
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


json_data = open(os.path.dirname(os.path.abspath(__file__)) + '/../config.json')
data = json.load(json_data)


class Publish(Publishing):
    def __init__(self, post_id, title, description, link_url, image_url,
                 date_from, date_until, option, channel_id="ICTV Superform Test", state=-1):
        self.post_id = post_id
        self.channel_id = channel_id
        self.state = state
        self.title = title
        self.description = description
        self.link_url = link_url
        self.image_url = image_url
        self.date_from = date_from
        self.date_until = date_until
        self.extra = json.dumps(option)


def test_get_module_ictv():
    """
    Tests if the module ictv is active
    :return:
    """
    with app.app_context():
        module_name = "ictv"
        m = get_module_full_name(module_name)
        assert m == "superform.plugins.ictv"


def test_run():
    with app.app_context():
        my_publy = Publish(0,
                           "TitleTestForTheICTV_ChannelSlide1",
                           "DescriptionTestForTheICTV_ChannelSlide1",
                           "",
                           None,
                           datetime.datetime.strptime('Jun 29 2018  1:33PM', '%b %d %Y %I:%M%p'),
                           datetime.datetime.strptime('Jun 30 2018  1:33PM', '%b %d %Y %I:%M%p'),
                           {"ictv_list":
                               [{'title-1':{'text': 'Awesome title!'},
                                 'subtitle-1':{'text': 'Subtile subtitle'},
                                 'text-1':{'text': 'Very long textual text here'},
                                 'logo-1':{'src': 'michelfra.svg'},
                                 'image-1':{"src": "http://thecatapi.com/api/images/get"},
                                 'background-1':"color",
                                 'duration':5000}]
                            })
        run = ictv.run(my_publy,None)
        assert run == True

        # GET the capsule /capsules/1
        urlData = "http://www.mocky.io/v2/5c099a843500006c00a85e07"
        webURL = urllib.request.urlopen(urlData)
        assert 200 == webURL.getcode()
        data = webURL.read()
        encoding = webURL.info().get_content_charset('utf-8')

        # Header data test
        data_header = json.loads(data.decode(encoding))['slides'][0]
        assert 5000 == data_header['duration']
        assert 1 == data_header['id']

        # Content data test
        data_content = data_header['content']
        assert {'text': 'Awesome title!'} == data_content['title-1']
        assert {'text': 'Subtile subtitle'} == data_content['subtitle-1']
        assert {'text': 'Very long textual text here'} == data_content['text-1']
        assert {'src': 'http://thecatapi.com/api/images/get'} == data_content['image-1']
        assert {'src': 'michelfra.svg'} == data_content['logo-1']

        # DELETE the capsule capsules/1
        urlData = "http://www.mocky.io/v2/5c09a10c3500006c00a85e10"
        webURL = urllib.request.urlopen(urlData)
        assert 204 == webURL.getcode()