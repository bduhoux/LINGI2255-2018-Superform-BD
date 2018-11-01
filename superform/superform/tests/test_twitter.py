import json
import random

import plugins.Twitter as Twitter
from superform import app
import twitter
from superform.models import Publishing

cha_conf = json.dumps({"Access token": "1052533183151886336-RBoq1epkAOeRfGdd2pBrbi9uTxQBv6",
                       "Access token secret": "vqM1nqgcst0uNDSryuMGjhCjT9ldCj4rFUpfxJfDzuTzc"})  # Getted from db
with app.app_context():
    twit = Twitter.get_api(cha_conf)  # We'll need this variable for other tests


class Publish(Publishing):
    def __init__(self, post_id, title, description, link_url, image_url,
                 date_from, date_until, option=None, channel_id="Twitter Superform Test", state=-1):
        if option is None:
            option = {"truncated": False}
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
    The following functions will test the getStatus() function in Twitter module.
    """


def test_publishing_short():
    """
    This function will test a short publication

     """
    with app.app_context():
        my_publy = Publish(0, "Why Google+ is still relevant, even though it will soon cease to exist",
                           "And Jesus said : This is my body",
                           "www.chretienDeTroie.fr",
                           None, " 24-12-2018", "12-12-2222")
        c = Twitter.getStatus(my_publy)
        assert c == my_publy.description + " " + my_publy.link_url
        assert len(c) <= 280


def test_publishing_long_truncated():
    """
    This function will test to send long random publications with the parameter truncated at True
    """
    with app.app_context():
        for i in range(20):
            leng = int(random.random() * 200 + 281)
            title = "Why Twitter is better than Google+"
            link_url = "www.chretienDeTroieOlalalalala.fr"
            message = ""
            for _ in range(leng):
                message += "abcdefghijklmnopqrstuvwxyz"[int(random.random() * 26)]
            my_publy = Publish(i, title, message, link_url,
                               None, " 24-12-2018", "12-12-2222", option={"truncated": True})
            c = Twitter.getStatus(my_publy)
            u = my_publy.description[:(280 - len(" ") - len(my_publy.link_url[:23]))]
            assert my_publy.post_id == i
            assert c == u + " " + my_publy.link_url
            assert my_publy.title == title
            assert my_publy.link_url == link_url
            len_end = 1 + len(link_url)
            len_url_short = twitter.twitter_utils.calc_expected_status_length(" " + link_url)
            assert c == message[:280 - len_end] + c[280 - len_end:]
            assert len(c) == 280 + len_end - len_url_short


def test_publishing_long_truncated_2():
    """
    This function will test to send long random publications with the parameter truncated at True
    """
    with app.app_context():
        for i in range(20):
            leng = int(random.random() * 200 + 281)
            title = "Why Twitter is better than Google+"
            link_url = ""
            message = ""
            for _ in range(leng):
                message += "abcdefghijklmnopqrstuvwxyz"[int(random.random() * 26)]
            my_publy = Publish(i, title, message, link_url,
                               None, " 24-12-2018", "12-12-2222", option={"truncated": True})
            c = Twitter.getStatus(my_publy)
            u = my_publy.description[:280]
            assert my_publy.post_id == i
            assert c == u
            assert my_publy.title == title
            assert my_publy.link_url == link_url
            assert c == message[:280] + c[280:]
            assert len(c) == 280


def test_publishing_long_not_truncated():
    """
    This function will test to send long random publications with the parameter truncated at False
    """
    with app.app_context():
        for i in range(20):
            leng = int(random.random() * 200 + 281)
            title = "Why Twitter is better than Google+"
            link_url = "www.chretienDeTroieOlalalalala.fr"
            message = ""
            for _ in range(leng):
                message += "abcdefghijklmnopqrstuvwxyz"[int(random.random() * 26)]
            my_publy = Publish(i, title, message, link_url,
                               None, " 24-12-2018", "12-12-2222", option={"truncated": False})
            c = Twitter.getStatus(my_publy)
            assert my_publy.post_id == i
            assert my_publy.title == title
            assert my_publy.link_url == link_url
            len_end = 1 + len(link_url)
            assert c == message[:leng - len_end] + c[leng - len_end:]
            assert len(c) <= leng + len_end


"""
The following functions will test the run() and publish_with_continuation() (since it is used by run() )
functions in Twitter module.
"""


def test_run_short():
    with app.app_context():
        my_publy = Publish(0, "Why Google+ is still relevant, even though it will soon cease to exist",
                           "And Jesus said : This is my body", "",
                           None, " 24-12-2018", "12-12-2222")
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
                           None, " 24-12-2018", "12-12-2222", option={"truncated": True})
        a = json.loads(str(Twitter.run(my_publy, cha_conf)))
        status = json.loads(str(twit.GetStatus(a["id"])))
        twit.DestroyStatus(a["id"])
        assert status["full_text"] == my_publy.description[0:280]

def test_run_not_truncated():
    with app.app_context():
        leng = int(random.random() * 200 + 281)
        title = "Why Twitter is better than Google+"
        link_url = ""
        message = ""
        for _ in range(leng):
            message += "abcdefghijklmnopqrstuvwxyz"[int(random.random() * 26)]
        my_publy = Publish(0, title, message, link_url,
                           None, " 24-12-2018", "12-12-2222", option={"truncated": False})
        list = Twitter.run(my_publy,cha_conf)
        index = 0
        for twet in list:
            a = json.loads(str(twet))
            status = json.loads(str(twit.GetStatus(a["id"])))
            twit.DestroyStatus(a["id"])
            assert status["full_text"] == my_publy.description[index:index+len(status["full_text"])]
            index += index + len(a["full_text"])

