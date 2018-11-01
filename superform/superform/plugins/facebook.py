from flask import current_app
import json
import facebook

FIELDS_UNAVAILABLE = ['Title', 'Description']  # list of field names that are not used by your module

CONFIG_FIELDS = ["page_id",
                 "access_token"]  # This lets the manager of your module enter data that are used to communicate with other services.


def run(publishing, channel_config):  # publishing:DB channelconfig:DB channel
    page_id = get_page_id(channel_config)  # data sur le sender ds channelconfig(= dictionnaire)
    access_token = get_access_token(channel_config)  # data sur le receiver ds channelconfig(= dictionnaire)

    cfg = get_config(page_id, access_token)
    api = get_api(cfg)

    msg = get_message(publishing)
    link = get_link(publishing)
    status = api.put_object(
        parent_object="me",
        connection_name="feed",
        message=msg,
        link=link
    )



def get_api(cfg):
    graph = facebook.GraphAPI(cfg['access_token'])
    return graph


def get_page_id(config):
    json_data = json.loads(config)
    return json_data['page_id']


def get_access_token(config):
    json_data = json.loads(config)
    return json_data['access_token']


def get_config(page_id, access_token):
    cfg = {
        "page_id": page_id,  # Step 1
        "access_token": access_token  # Step 3
    }
    return cfg


def get_message(publishing):
    return publishing.title + "\n\n" + publishing.description


def get_link(publishing):
    return publishing.link_url