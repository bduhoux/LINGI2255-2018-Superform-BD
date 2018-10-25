
import datetime
import os
import tempfile

import json
import unittest
import random

import plugins.Twitter as Twitter
from superform import app
import twitter

cha_conf = json.dumps({"Access token": "1052533183151886336-RBoq1epkAOeRfGdd2pBrbi9uTxQBv6",
                       "Access token secret": "vqM1nqgcst0uNDSryuMGjhCjT9ldCj4rFUpfxJfDzuTzc"}) #Getted from db


class Publishing:
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


class TestTwitter(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        with app.app_context():
            self.twit = Twitter.get_api(cha_conf)  # We'll need this variable for other tests

    def test_login(self):
        with app.app_context():
            a = self.twit.VerifyCredentials()
            self.assertIsNotNone(a)
            self.assertEqual(a.name, "SuperformDev01")

    def test_publishing_short(self):
        with app.app_context():
            my_publy = Publishing(0, "Why Google+ is still relevant, even though it will soon cease to exist",
                                  "And Jesus said : This is my body",
                                  "www.chretienDeTroie.fr",
                                  None, " 24-12-2018", "12-12-2222")
            twit = Twitter.get_api(cha_conf)
            c = Twitter.getStatus(my_publy, twit)
            self.assertEqual(c, my_publy.description + " " + my_publy.link_url)
            self.assertLessEqual(len(c), 280)

    def test_publishing_long_truncated(self):
        with app.app_context():
            leng = 280
            title = "Why Twitter is better than Google+"
            link_url = "www.chretienDeTroieOlalalalala.fr"
            message = ""
            for _ in range(leng):
                message += "abcdefghijklmnopqrstuvwxyz"[int(random.random()*26)]
            my_publy = Publishing(0, title, message, link_url,
                                  None, " 24-12-2018", "12-12-2222", option={"truncated": True})
            twit = Twitter.get_api(cha_conf)
            c = Twitter.getStatus(my_publy, twit)
            u = my_publy.description[:(280-len(" ")-len(my_publy.link_url[:23]))]
            self.assertEqual(c, u + " " + my_publy.link_url)
            #self.assertLessEqual(len(c), 280)
            self.assertEqual(my_publy.title, title)
            self.assertEqual(my_publy.link_url, link_url)
            len_end = 1+len(link_url)
            len_url_short = twitter.twitter_utils.calc_expected_status_length(" " + link_url)
            self.assertEqual(c, message[:280-len_end] + c[280-len_end:])
            self.assertEqual(len(c), 280+len_end - len_url_short)

    def test_publishing_long_not_truncated(self):
        with app.app_context():
            leng = 500
            title = "Why Twitter is better than Google+"
            link_url = "www.chretienDeTroieOlalalalala.fr"
            message = ""
            for _ in range(leng):
                message += "abcdefghijklmnopqrstuvwxyz"[int(random.random()*26)]
            my_publy = Publishing(0, title, message, link_url,
                                  None, " 24-12-2018", "12-12-2222", option={"truncated": False})
            twit = Twitter.get_api(cha_conf)
            c = Twitter.getStatus(my_publy, twit)
            self.assertEqual(my_publy.title, title)
            self.assertEqual(my_publy.link_url, link_url)
            len_end = 1+len(link_url)
            self.assertEqual(c, message[:leng-len_end] + c[leng-len_end:])
            self.assertLessEqual(len(c), leng+len_end)




if __name__ == "__main__":
    unittest.main()