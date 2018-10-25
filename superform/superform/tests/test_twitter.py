import json
import unittest
import random

import plugins.Twitter as Twitter
from superform import app
import twitter
from superform.models import Publishing

cha_conf = json.dumps({"Access token": "1052533183151886336-RBoq1epkAOeRfGdd2pBrbi9uTxQBv6",
                       "Access token secret": "vqM1nqgcst0uNDSryuMGjhCjT9ldCj4rFUpfxJfDzuTzc"})  # Getted from db


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


class TestTwitter(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        with app.app_context():
            self.twit = Twitter.get_api(cha_conf)  # We'll need this variable for other tests

    def test_login(self):
        """
        This function tests the login to the application
        """
        with app.app_context():
            a = self.twit.VerifyCredentials()
            self.assertIsNotNone(a)
            self.assertEqual(a.name, "SuperformDev01")


    """
    The following functions will test the getStatus() function in Twitter module.
    """
    def test_publishing_short(self):
        """
        This function will test a short publication
        """
        with app.app_context():
            my_publy = Publish(0, "Why Google+ is still relevant, even though it will soon cease to exist",
                                  "And Jesus said : This is my body",
                                  "www.chretienDeTroie.fr",
                                  None, " 24-12-2018", "12-12-2222")
            twit = Twitter.get_api(cha_conf)
            c = Twitter.getStatus(my_publy, twit)
            self.assertEqual(c, my_publy.description + " " + my_publy.link_url)
            self.assertLessEqual(len(c), 280)

    def test_publishing_long_truncated(self):
        """
        This function will test to send long random publications with the parameter truncated at True
        """
        with app.app_context():
            for i in range(20):
                leng = int(random.random()*200+281)
                title = "Why Twitter is better than Google+"
                link_url = "www.chretienDeTroieOlalalalala.fr"
                message = ""
                for _ in range(leng):
                    message += "abcdefghijklmnopqrstuvwxyz"[int(random.random()*26)]
                my_publy = Publish(i, title, message, link_url,
                                      None, " 24-12-2018", "12-12-2222", option={"truncated": True})
                twit = Twitter.get_api(cha_conf)
                c = Twitter.getStatus(my_publy, twit)
                u = my_publy.description[:(280-len(" ")-len(my_publy.link_url[:23]))]
                self.assertEqual(my_publy.post_id, i)
                self.assertEqual(c, u + " " + my_publy.link_url)
                self.assertEqual(my_publy.title, title)
                self.assertEqual(my_publy.link_url, link_url)
                len_end = 1+len(link_url)
                len_url_short = twitter.twitter_utils.calc_expected_status_length(" " + link_url)
                self.assertEqual(c, message[:280-len_end] + c[280-len_end:])
                self.assertEqual(len(c), 280+len_end - len_url_short)

    def test_publishing_long_truncated_2(self):
        """
        This function will test to send long random publications with the parameter truncated at True
        """
        with app.app_context():
            for i in range(20):
                leng = int(random.random()*200+281)
                title = "Why Twitter is better than Google+"
                link_url = ""
                message = ""
                for _ in range(leng):
                    message += "abcdefghijklmnopqrstuvwxyz"[int(random.random()*26)]
                my_publy = Publish(i, title, message, link_url,
                                      None, " 24-12-2018", "12-12-2222", option={"truncated": True})
                twit = Twitter.get_api(cha_conf)
                c = Twitter.getStatus(my_publy, twit)
                u = my_publy.description[:280]
                self.assertEqual(my_publy.post_id, i)
                self.assertEqual(c, u)
                self.assertEqual(my_publy.title, title)
                self.assertEqual(my_publy.link_url, link_url)
                self.assertEqual(c, message[:280] + c[280:])
                self.assertEqual(len(c), 280)

    def test_publishing_long_not_truncated(self):
        """
        This function will test to send long random publications with the parameter truncated at False
        """
        with app.app_context():
            for i in range(20):
                leng = int(random.random()*200+281)
                title = "Why Twitter is better than Google+"
                link_url = "www.chretienDeTroieOlalalalala.fr"
                message = ""
                for _ in range(leng):
                    message += "abcdefghijklmnopqrstuvwxyz"[int(random.random()*26)]
                my_publy = Publish(i, title, message, link_url,
                                      None, " 24-12-2018", "12-12-2222", option={"truncated": False})
                twit = Twitter.get_api(cha_conf)
                c = Twitter.getStatus(my_publy, twit)
                self.assertEqual(my_publy.post_id, i)
                self.assertEqual(my_publy.title, title)
                self.assertEqual(my_publy.link_url, link_url)
                len_end = 1+len(link_url)
                self.assertEqual(c, message[:leng-len_end] + c[leng-len_end:])
                self.assertLessEqual(len(c), leng+len_end)


    """
    The following functions will test the run() and publish_with_continuation() (since it is used by run() )
    functions in Twitter module.
    """
    def test_run_short(self):
        with app.app_context():
            twit = Twitter.get_api(cha_conf)
            my_publy = Publish(0, "Why Google+ is still relevant, even though it will soon cease to exist",
                                 "And Jesus said : This is my body", "",
                                  None, " 24-12-2018", "12-12-2222")
            a = json.loads(str(Twitter.run(my_publy, cha_conf)))
            twit.DestroyStatus(a["id"])
            self.assertEqual(a["text"],
                             my_publy.description)  # We do not care about the www. in a tweet url



if __name__ == "__main__":
    unittest.main()
