import json
import os
import random

import superform.plugins.Twitter as Twitter
from superform import app
from superform.models import Publishing


json_data = open(os.path.dirname(os.path.abspath(__file__)) + '/../config.json')
data = json.load(json_data)

cha_conf = json.dumps({"Access token": data["TWITTER_TEST_ACESS TOKEN"],
                       "Access token secret": data["TWITTER_TEST_ACESS TOKEN_SECRET"]})  # Getted from db
with app.app_context():
    twit = Twitter.get_api(cha_conf)  # We'll need this variable for other tests


class Publish(Publishing):
    def __init__(self, post_id, title, description, link_url, image_url,
                 date_from, date_until, option, channel_id="Twitter Superform Test", state=-1):
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


def test_login():
    """
    This function tests the login to the application
    """
    with app.app_context():
        a = twit.VerifyCredentials()
        assert a
        assert a.name == "SuperformDev01"


"""
The following functions will test the run() (and publish list since run using it)
functions in Twitter module.
"""


def test_run_short():
    with app.app_context():
        my_publy = Publish(0, "Why Google+ is still relevant, even though it will soon cease to exist",
                           "And Jesus said : This is my body", "",
                           None, " 24-12-2018", "12-12-2222", {"tweet_list": [(0, "And Jesus said : This is my body")]})
        a = json.loads(str(Twitter.run(my_publy, cha_conf)[0]))
        twit.DestroyStatus(a["id"])
        assert a["text"] == my_publy.description  # We do not care about the www. in a tweet url


def test_run_truncated():
    with app.app_context():
        leng = int(random.random() * 200 + 281)
        title = "Why Twitter is better than Google+"
        link_url = ""
        message = ""
        for _ in range(leng):
            message += "abcdefghijklmnopqrstuvwxyz"[int(random.random() * 26)]
        my_publy = Publish(0, title, message, link_url,
                           None, " 24-12-2018", "12-12-2222", {"tweet_list": [(0, message[0:280])]})
        a = json.loads(str(Twitter.run(my_publy, cha_conf)[0]))
        status = json.loads(str(twit.GetStatus(a["id"])))
        twit.DestroyStatus(a["id"])
        assert status["full_text"] == my_publy.description[0:280]
