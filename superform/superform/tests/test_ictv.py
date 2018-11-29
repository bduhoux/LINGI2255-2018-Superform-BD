import json
import os
import random

from flask import current_app
from superform.plugins import ictv
from superform import app
from superform.models import Publishing

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


def test_run_one_slide():
    with app.app_context():
        my_publy = Publish(0, "TitleTestForTheICTV_ChannelSlide1",
                           "DescriptionTestForTheICTV_ChannelSlide1", "",
                           None, " 29-11-2018", "30-11-2018",
                           {"ictv_list": [("SlideTitle1", "SubtitleSlide1", "TextSlide1", "", "", "", 1000)]})
        print(json.loads(str(ictv.run(my_publy)[0])))
        # a = json.loads(str(ictv.run(my_publy)[0]))
        # assert a["text"] == my_publy.description  # We do not care about the www. in a tweet url

