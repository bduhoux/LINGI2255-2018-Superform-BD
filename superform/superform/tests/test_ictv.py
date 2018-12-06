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
