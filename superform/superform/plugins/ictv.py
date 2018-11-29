from flask import current_app
import json
from superform import app

FIELDS_UNAVAILABLE = ['Title', 'Description', 'Linkurl', 'Image']
CONFIG_FIELDS = []


def run(publishing):

    print("ICTV_LIST :")
    print(json.loads(publishing.extra)['ictv_list'][0])

    # status_list = json.loads(publishing.extra)['ictv_list'][0]
    # if publishing.image_url is not '':
    #     return publish_list(status_list, image=publishing.image_url)
    # else:
    #     return publish_list(status_list)


# def publish_list(status_list, image=None):
#     a = []
#     if status_list[len(status_list) - 1] != "":
#         a.append(twitter_api.PostUpdate(status_list[len(status_list) - 1], image))
#     return a
