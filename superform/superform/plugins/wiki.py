import json
import urllib.request


FIELDS_UNAVAILABLE = ['Title','Description'] #list of field names that are not used by your module

# appelé dans publishings.py
def run(publishing,channel_config): #publishing:DB channelconfig:DB channel
    title = publishing.title
    body = publishing.description
    picture = publishing.image_url
    link = publishing.link_url

    int = title.replace(" ","")
    url = "http://localhost:8000/pmwiki.php?n=" + int

    page = urllib.request.urlopen(url)

    title = "(:Title " + title + ":)"
