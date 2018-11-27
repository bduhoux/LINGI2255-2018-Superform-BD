from flask import current_app
import twitter
import json
from superform.run_plugin_exception import RunPluginException

FIELDS_UNAVAILABLE = ['Title']
FILES_MANDATORY = ['Description']
CONFIG_FIELDS = ["Access token", "Access token secret"]


def run(publishing, channel_config):
    """
    Publishes on a Twitter channel the publication contained in publishing.
    :param publishing: a dictionary containing the elements of the publication
    :param channel_config: The configuration of the Twitter channel used for publishing
    """
    json_data = json.loads(channel_config)
    if 'Access token' in json_data and 'Access token secret' in json_data:

        # Get Twitter API
        twitter_api = get_api(channel_config)

        statuslist = [y for x, y in json.loads(publishing.extra)['tweet_list']]
        if publishing.image_url is not '':
            return publish_list(statuslist, twitter_api, media=publishing.image_url)
        else:
            return publish_list(statuslist, twitter_api)
    else:
        raise RunPluginException('Please configure the channel first')


def get_channel_fields(form, chan):
    """
    :param form:
    :param chan:
    :return:
    """
    tweet_list = []
    end = False
    i = 1
    while not end:
        if chan is None:
            tweet = form.get('tweet_' + str(i))
        else:
            tweet = form.get(chan + '_tweet_' + str(i))
        if tweet is not None:
            tweet_list.append((str(i), tweet))
        else:
            end = True
        i += 1
    extra = dict()
    extra['tweet_list'] = tweet_list
    return extra


def get_api(channel_config):
    """
    Returns a twitter.Api() object for the Twitter account described in the channel configuration
    :param channel_config: A json string containing the configuration of the channel
    :return: a Twitter.Api() object
    """
    json_data = json.loads(channel_config)
    consumer_key = current_app.config["TWITTER_APIKEY"]
    consumer_secret = current_app.config["TWITTER_APISECRET"]
    access_token = json_data['Access token']
    access_token_secret = json_data['Access token secret']
    return twitter.Api(consumer_key=consumer_key,
                       consumer_secret=consumer_secret,
                       access_token_key=access_token,
                       access_token_secret=access_token_secret,
                       tweet_mode='extended')


def publish_list(statuslist, twitter_api, media=None):
    a = []
    for status in statuslist[:-1]:
        if status != "":
            a.append(twitter_api.PostUpdate(status))
    if statuslist[len(statuslist) - 1] != "":
        a.append(twitter_api.PostUpdate(statuslist[len(statuslist) - 1], media))
    return a
