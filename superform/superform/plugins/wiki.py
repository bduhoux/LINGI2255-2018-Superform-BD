import json
from urllib.parse import urlencode
from urllib.request import Request, urlopen


FIELDS_UNAVAILABLE = [] #list of field names that are not used by your module

CONFIG_FIELDS = ["Author", "Wiki's url"]  # This lets the manager of your module enter data that are used to communicate with other services.


# appelé dans publishings.py
def run(publishing, channel_config):  # publishing:DB channelconfig:DB channel
    author = get_author(channel_config)  # data sur le sender ds channelconfig(= dictionnaire)
    url = get_url(channel_config)  # data sur le receiver ds channelconfig(= dictionnaire)

    title = publishing.title
    page = 'PmWiki.'+title

    picture = publishing.image_url
    link = publishing.link_url

    post_fields = {'n': page, 'text': publishing.description, 'action': 'edit', 'post': 1, 'author': author}

    request = Request(url, urlencode(post_fields).encode())

    response = urlopen(request)


def get_author(config):
    json_data = json.loads(config)
    return json_data["Author"]


def get_url(config):
    json_data = json.loads(config)
    return json_data["Wiki's url"]


def delete(titre, channel_config):
    author = get_author(channel_config)  # data sur le sender ds channelconfig(= dictionnaire)
    url = get_url(channel_config)  # data sur le receiver ds channelconfig(= dictionnaire)
    page = 'PmWiki.'+titre

    post_fields = {'n': page, 'text': "delete", 'action': 'edit', 'post': 1, 'author': author}
    request = Request(url, urlencode(post_fields).encode())

    try:
        urlopen(request)
    except:
        pass
