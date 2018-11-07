import json
from urllib.parse import urlencode
from urllib.request import Request, urlopen


FIELDS_UNAVAILABLE = [] #list of field names that are not used by your module

CONFIG_FIELDS = ["author"]  # This lets the manager of your module enter data that are used to communicate with other services.


# appelé dans publishings.py
def run(publishing,channel_config): #publishing:DB channelconfig:DB channel
    title = publishing.title
    page = 'PmWiki.'+title

    picture = publishing.image_url
    link = publishing.link_url

    url = "http://localhost:8001/pmwiki.php"
    post_fields = {'n':page,'text':publishing.description,'action':'edit','post':1}

    request = Request(url, urlencode(post_fields).encode())

    response = urlopen(request)
    print(response.read())