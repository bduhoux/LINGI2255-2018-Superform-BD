import json
from slackclient import SlackClient

FIELDS_UNAVAILABLE = []
# list of field names that are not used by your module

CONFIG_FIELDS = ['token']


# This lets the manager of your module enter data that are used to communicate with other services.


# appelé dans publishings.py
def run(publishing, channel_config):
    json_data = json.loads(channel_config)
    token = json_data['token']
    slack_client = SlackClient(token)

    channels = slack_client.api_call(
        "conversations.list"
    )
    if channels['ok']:
        for channel in channels['channels']:
            if channel['is_member']:
                channelid = channel['id']
                slack_client.api_call(
                    "chat.postMessage",
                    channel=channelid,
                    text="hello"
                )
    else:
        # TODO: erreur à afficher
        pass
