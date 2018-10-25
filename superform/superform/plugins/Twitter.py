from flask import current_app
import twitter
import json

FIELDS_UNAVAILABLE = ['Title']
CONFIG_FIELDS = ["Access token", "Access token secret"]

def run(publishing,channel_config):

    # Get Twitter API
    twitter_api = get_api(channel_config)
    # Create body
    status = getStatus(publishing, twitter_api)
    print(twitter.twitter_utils.calc_expected_status_length(status, short_url_length=23))
    # twitter_test(status, json.loads(publishing.extra)["truncated"], continuation="[...]"
    # , **{"media": publishing.image_url})

    # we don't need to deal with too long text
    if json.loads(publishing.extra)["truncated"]:
        if publishing.image_url is not '':
            twitter_api.PostUpdate(status, media=publishing.image_url)
        else:
            twitter_api.PostUpdate(status)

    # we need to deal with too long text
    else:
        cont = "[" + u"\u2026" + "]"
        if publishing.image_url is not '':
            twitter_api.PostUpdates(status, continuation=cont, **{"media": publishing.image_url, "verify_status_length": False})
        else:
            twitter_api.PostUpdates(status, continuation=cont, **{"verify_status_length": False})


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
                       access_token_secret=access_token_secret)


def getStatus(publishing, twitter_api):
    if json.loads(publishing.extra)["truncated"]:
        status = publishing.description[:279]
        if publishing.link_url is not '':
            status = status[:279-1-twitter_api.GetShortUrlLength(https=True)] + " "+ publishing.link_url
    else:
        status = publishing.description
        if publishing.link_url is not '':
            status = status + " " + publishing.link_url
    return status.replace('\r', '')


def twitter_test(status, truncated, continuation, **kwargs):
    print(status)
    print(truncated)
    print(continuation)
    print(kwargs["media"])
    print()
