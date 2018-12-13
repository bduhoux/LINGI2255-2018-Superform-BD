from flask import request, jsonify, Blueprint, url_for, redirect, abort, session
import json
import facebook

from superform.run_plugin_exception import RunPluginException
from superform.models import db, Post, Publishing, Channel

# facebook_plugin = Blueprint("facebook_plugin", __name__)
facebook_plugin = Blueprint("facebook_plugin", "superform.plugins.facebook")

FIELDS_UNAVAILABLE = []  # list of field names that are not used by your module

CONFIG_FIELDS = ["page_id", "app_id"]  # This lets the manager of your module enter data that are used to communicate with other services.

facebook_is_connected = False

fb_token = 0


def run(publishing, channel_config):  # publishing:DB channelconfig:DB channel
    page_id = get_page_id()
    access_token = fb_token # == 0 alors pas connecté
    if str(access_token) == "0":
        print("token error, are you sure you are connected to facebook?")
        facebook_is_connected = False
    else:
        facebook_is_connected = True
        cfg = get_config(page_id, access_token)
        api = get_api(cfg)

        msg = get_message(publishing)
        pub_link = get_link(publishing)
        image = get_image(publishing)

        try:
            status1 = api.put_object(
                parent_object="me",
                connection_name="feed",
                message=msg,
                link=pub_link
            )

            put_extra(publishing, status1['id'])
        except:
            raise RunPluginException('Please check your connection to facebook!')


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


def get_api(cfg):
    graph = facebook.GraphAPI(cfg['access_token'])
    return graph


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


def delete(post_id):
    try:
        api = get_api(get_config(get_page_id(), fb_token))
        api.delete_object(post_id)
    except:
        raise RunPluginException('Please check your internet connection or if this post still exists on your facebook page!')


def put_extra(publishing, post_id):
    pub = db.session.query(Publishing).filter(Publishing.post_id == publishing.post_id, Publishing.channel_id == publishing.channel_id).first()
    pub.date_from = publishing.date_from
    pub.date_until = publishing.date_until
    pub.title = publishing.title
    pub.description = publishing.description
    pub.link_url = publishing.link_url
    pub.image_url = publishing.image_url
    extra = dict()
    extra['facebook_post_id'] = post_id
    pub.extra = json.dumps(extra)
    db.session.commit()


