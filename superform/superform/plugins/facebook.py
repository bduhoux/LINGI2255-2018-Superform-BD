from flask import request, jsonify, Blueprint, url_for, redirect, abort
import json
import facebook
from superform.models import db, Post, Publishing, Channel

# facebook_plugin = Blueprint("facebook_plugin", __name__)
facebook_plugin = Blueprint("facebook_plugin", "superform.plugins.facebook")

FIELDS_UNAVAILABLE = ['Title', 'Description']  # list of field names that are not used by your module

CONFIG_FIELDS = ["page_id", "app_id"]  # This lets the manager of your module enter data that are used to communicate with other services.

facebook_is_connected = False

fb_token = 0


def run(publishing, channel_config):  # publishing:DB channelconfig:DB channel
    print(9)
    page_id = get_page_id()
    access_token = fb_token # == 0 alors pas connecté
    print("access_token = " + str(access_token))
    if str(access_token) == "0":
        print("token error, are you sure you are connected to facebook?")
        facebook_is_connected = False
    else:
        facebook_is_connected = True
        cfg = get_config(page_id, access_token)
        api = get_api(cfg)

        msg = get_message(publishing)
        link = get_link(publishing)
        image = get_image(publishing)

        status1 = api.put_object(
            parent_object="me",
            connection_name="feed",
            message=msg,
            link=link

        )

def get_api(cfg):
    graph = facebook.GraphAPI(cfg['access_token'])
    return graph

"""
def get_page_id(config):
    json_data = json.loads(config)
    return json_data['page_id']
"""

@facebook_plugin.route('/appid')
def get_app_id():
    config = db.session.query(Channel).filter(Channel.module == "superform.plugins.facebook").first().config
    json_data = json.loads(config)
    app_id = json_data["app_id"]
    return jsonify(app_id)

@facebook_plugin.route('/pageid')
def get_page_id():
    config = db.session.query(Channel).filter(Channel.module == "superform.plugins.facebook").first().config
    json_data = json.loads(config)
    page_id = json_data["page_id"]
    return jsonify(page_id)

@facebook_plugin.route('/token', methods=['POST'])
def set_token():
    global fb_token
    data = request.get_data()
    jss = json.loads(data.decode("utf-8"))
    fb_token = jss['token']
    return jsonify(status = "success", data="ok")


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


def get_image(publishing):
    return publishing.image_url
