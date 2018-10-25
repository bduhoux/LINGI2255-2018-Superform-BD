from flask import current_app
import twitter
import json

FIELDS_UNAVAILABLE = ['Title']
CONFIG_FIELDS = ["Access token", "Access token secret"]


def run(publishing, channel_config):
    """
    Publishes on a Twitter channel the publication contained in publishing.
    :param publishing: a dictionary containing the elements of the publication
    :param channel_config: The configuration of the Twitter channel used for publishing
    """
    # Get Twitter API
    twitter_api = get_api(channel_config)
    # Create body
    status = getStatus(publishing, twitter_api)
    # twitter_test(status, json.loads(publishing.extra)["truncated"], continuation="[...]"
    # , **{"media": publishing.image_url})

    # we don't need to deal with too long text
    if json.loads(publishing.extra)["truncated"]:
        if publishing.image_url is not '':
            return twitter_api.PostUpdate(status, media=publishing.image_url)
        else:
            return twitter_api.PostUpdate(status)

    # we need to deal with too long text
    else:
        cont = "[" + u"\u2026" + "]"
        return publish_with_continuation(status, twitter_api, cont, media=None)


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
        status = publishing.description[:280]
        if publishing.link_url is not '':
            status = status[:280 - twitter.twitter_utils.calc_expected_status_length(" " + publishing.link_url)] \
                     + " " + publishing.link_url
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


def publish_with_continuation(status, twitter_api, continuation, media=None):
    short_status = ''
    words = status.split(" ")
    for word in words:
        while len(word) > 280:
            newlen = 280 - len(short_status + continuation) - 1
            short_status += word[:newlen]
            twitter_api.PostUpdate(short_status + continuation)
            word = word[newlen:]
            short_status = ''
        if short_status == '':
            new_short_status = short_status + word
        else:
            new_short_status = short_status + ' ' + word
        if twitter.twitter_utils.calc_expected_status_length(new_short_status + continuation) <= 280:
            short_status = new_short_status
        else:
            twitter_api.PostUpdate(short_status + continuation)
            short_status = word

    return twitter_api.PostUpdate(short_status, media=media)


def getBadUsernames(text):
    """ Returns a list of Twitter usernames found in text that don't refer to any Twitter account
    :param text: A string
    :return: A list of the nonexisting usernames in the text (if any)
    """
    # Get API
    twitter_api = get_api()
    # Find all usernames in text
    pattern = re.compile('\B@[a-zA-Z0-9_]+')
    tags = pattern.findall(text)
    # Check if usernames exist
    bad_usernames = []
    for tag in tags:
        try:
            user = twitter_api.GetUser(screen_name=tag[1:])
        except twitter.error.TwitterError:
            bad_usernames.append(tag)
    return bad_usernames
