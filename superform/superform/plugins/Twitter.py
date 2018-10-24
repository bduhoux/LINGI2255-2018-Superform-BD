from flask import current_app
import twitter
import json

FIELDS_UNAVAILABLE = ['Title']
CONFIG_FIELDS = ["Consumer key", "Consumer secret", "Access token", "Access token secret"]

def run(publishing,channel_config):
    # Get Twitter API
    twitter_api = get_api(channel_config)
    # Create body
    kwargs = get_update_kwargs(publishing)
    status = publishing.description
    continuation = '[...]' # String that will be appended to the messages if too many characters
    twitter_api.PostUpdate(status, continuation, **kwargs)

def get_api(channel_config):
    """
    Returns a twitter.Api() object for the Twitter account described in the channel configuration
    :param channel_config: A json string containing the configuration of the channel
    :return: a Twitter.Api() object
    """
    json_data = json.loads(channel_config)
    consumer_key = json_data['Consumer key']
    consumer_secret = json_data['Consumer secret']
    access_token = json_data['Access token']
    access_token_secret = json_data['Access token secret']
    return twitter.Api(consumer_key=consumer_key,
                       consumer_secret=consumer_secret,
                       access_token_key=access_token,
                       access_token_secret=access_token_secret)

def get_update_kwargs(publishing):
    """
    Returns a dictionary containing the options selected in publishing
    (see https://python-twitter.readthedocs.io/en/latest/twitter.html#twitter.api.Api.PostUpdate for the options)
    :param publishing:
    :return: a dictionary
    """
    pass