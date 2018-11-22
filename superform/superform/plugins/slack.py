import json
from slackclient import SlackClient

FIELDS_UNAVAILABLE = []
FILES_MANDATORY = ['Description']
# list of field names that are not used by your module

CONFIG_FIELDS = ['token', 'channel name']


# This lets the manager of your module enter data that are used to communicate with other services.

def run(publishing, channel_config):
    json_data = json.loads(channel_config)
    token = json_data['token']
    name = json_data['channel name']
    slack_client = SlackClient(token)

    message = make_message(publishing)

    channels = slack_client.api_call(
        "conversations.list"
    )
    if channels['ok']:
        for channel in channels['channels']:
            if channel['name'] == name:
                channelid = channel['id']
                slack_client.api_call(
                    "chat.postMessage",
                    channel=channelid,
                    text=message
                )
    else:
        # TODO: erreur à afficher
        pass

def make_message(publishing):
    message = ""
    if publishing.title:
        message = message + "*" + publishing.title + "*\n\n"

    message = message + publishing.description

    if publishing.link_url:
        message = message + "\n\n" + publishing.link_url

    if publishing.image_url:
        message = message + "\n\n" + publishing.image_url

    return message
