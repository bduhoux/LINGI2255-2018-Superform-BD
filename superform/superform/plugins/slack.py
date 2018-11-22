import json
import slackclient

FIELDS_UNAVAILABLE = []
# list of field names that are not used by your module

CONFIG_FIELDS = ['token']
# This lets the manager of your module enter data that are used to communicate with other services.


# appelé dans publishings.py
def run(publishing, channel_config):
   json_data = json.loads(channel_config)
   token = json_data['token']