from flask import current_app
import json
import facebook

FIELDS_UNAVAILABLE = ['Title','Description'] #list of field names that are not used by your module

CONFIG_FIELDS = ["page_id","access_token"] #This lets the manager of your module enter data that are used to communicate with other services.


def run(publishing,channel_config): #publishing:DB channelconfig:DB channel
    json_data = json.loads(channel_config)  # to a Python object
    page_id = json_data['page_id']  # data sur le sender ds channelconfig(= dictionnaire)

    access_token = json_data['access_token']  # data sur le receiver ds channelconfig(= dictionnaire)
    cfg = {
        "page_id": page_id,  # Step 1
        "access_token": access_token  # Step 3
    }
    api = get_api(cfg)


    msg = publishing.title + "\n\n" + publishing.description
    link = publishing.link_url
    status = api.put_object(
        parent_object="me",
        connection_name="feed",
        message=msg,
        link = link
    )


def get_api(cfg):
    graph = facebook.GraphAPI(cfg['access_token'])
    return graph