import json
import re
from urllib.parse import urlencode
from urllib.request import Request, urlopen


FIELDS_UNAVAILABLE = [] #list of field names that are not used by your module

CONFIG_FIELDS = ["Author", "Wiki's url", "Publication's group"]  # This lets the manager of your module enter data that are used to communicate with other services.


# appelé dans publishings.py
def run(publishing, channel_config):  # publishing:DB channelconfig:DB channel
    author = get_author(channel_config)
    url = get_url(channel_config)
    group = get_pubblication_group(channel_config)

    title = get_title(publishing)
    page = group + '.' + title
    description = get_description(publishing)

    picture = get_image(publishing)
    links = get_links(publishing)

    post_fields = {'n': page, 'text': description+links, 'action': 'edit', 'post': 1, 'author': author}
    request = Request(url, urlencode(post_fields).encode())
    response = urlopen(request)


def get_author(config):
    json_data = json.loads(config)
    return json_data["Author"]


def get_url(config):
    json_data = json.loads(config)
    return json_data["Wiki's url"]

def get_pubblication_group(config):
    json_data = json.loads(config)
    return json_data["Publication's group"]


def get_title(publishing):
    title = publishing.title
    title = re.sub('[^A-Za-z0-9]+', '', title)
    return title


def get_description(publishing):
    return publishing.description


def get_links(publishing):
    separated_links = re.split(',| ', publishing.link_url)
    links_with_tags = ""
    for link in separated_links:
        if link:
            links_with_tags = links_with_tags + "\n\n[["+link+"]]"
    return links_with_tags


def get_image(publishing):
    return publishing.image_url


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
