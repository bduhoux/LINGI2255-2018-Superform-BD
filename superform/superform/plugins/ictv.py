from flask import current_app
import json

FIELDS_UNAVAILABLE = ['Title', 'Description', 'Linkurl', 'Image']
CONFIG_FIELDS = []


def run(publishing):

    # status_list = [y for x, y in json.loads(publishing.extra)['capsules']]
    # if publishing.image_url is not '':
    #     if publishing.logo is not '':
    #         return publish_list(status_list, image=publishing.image_url, logo=publishing.logo)
    #     else:
    #         return publish_list(status_list, image=publishing.image_url)
    # else:
    #     return publish_list(status_list)

    print(publishing)


# def publish_list(statuslist, image=None, logo=None):
#     a = []
#     for status in statuslist[:-1]:
#         a.append(status)
#     a.append(statuslist[len(statuslist) - 1], image, logo)
#     return a
