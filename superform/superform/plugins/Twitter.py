from flask import current_app
import twitter
import json

FIELDS_UNAVAILABLE = ['Title']
FILES_MANDATORY = ['Description']
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
    status = getStatus(publishing)
    # We don't need to deal with too long text
    if json.loads(publishing.extra)["truncated"]:
        if publishing.image_url is not '':
            return twitter_api.PostUpdate(status, media=publishing.image_url)
        else:
            return twitter_api.PostUpdate(status)
    # We need to deal with too long text
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


def getStatus(publishing):
    """
    Create the content of a tweet truncated if publishing.extra["truncated"] is true.
    The content of a tweet is the description and the url (if any) separated by a space.
    If we need to truncate the content the description is truncated an not the url
    :param publishing: a dictionary containing the elements of the publication
    :return: the content of the tweet according to the specification above
    """
    #if we need to truncate the text
    if json.loads(publishing.extra)["truncated"]:
        #without link we limit the description to 280 characters
        status = publishing.description[:280]
        if publishing.link_url is not '':
            # with link we limit the description to 280 characters- the size of the link and the space
            status = status[:280 - twitter.twitter_utils.calc_expected_status_length(" " + publishing.link_url)] \
                     + " " + publishing.link_url
    # if we don't need to truncate the text
    else:
        status = publishing.description
        if publishing.link_url is not '':
            status = status + " " + publishing.link_url
    # \r sometimes create some problems in the count of characters so we delete all the occurence
    return status.replace('\r', '')

def publish_with_continuation(status, twitter_api, continuation, media=None):
    """
    Publish the content of status in a tweet or more if necessary. If many tweet the first tweets are append with continuation.
    The media is linked to the last tweet
    (the implementation of this function in python-twitter API is buggy)
    :param status: the text to publish with the tweet
    :param twitter_api: a Twitter.Api() object
    :param continuation: a String that will be put at the end of a tweet to indicate that the status spans over
    multiple tweets
    :param media: the media to attach at the end of the tweet
    :return: the last tweet we send on twitter
    """
    # the content of the current tweet
    short_status = ''
    # the different words in the tweet
    words = status.split(" ")
    for word in words:
        # deal with words with more than 280 characters
        while len(word) > 280:
            newlen = 280 - len(short_status + continuation) - 1
            short_status += word[:newlen]
            twitter_api.PostUpdate(short_status + continuation)
            word = word[newlen:]
            short_status = ''

        # test to add the next word
        if short_status == '':
            new_short_status = short_status + word
        else:
            new_short_status = short_status + ' ' + word

        # if we can add the next word we add it
        if twitter.twitter_utils.calc_expected_status_length(new_short_status + continuation) <= 280:
            short_status = new_short_status
        # if we can't we publish
        else:
            twitter_api.PostUpdate(short_status + continuation)
            short_status = word

    # we publish the last tweet with the media attached
    return twitter_api.PostUpdate(short_status, media=media)


def publish_list(statuslist, twitter_api, continuation, media=None):
    for status in statuslist[:-1]:
        twitter_api.PostUpdate(status + continuation)
    twitter_api.PostUpdate(status + continuation, media)