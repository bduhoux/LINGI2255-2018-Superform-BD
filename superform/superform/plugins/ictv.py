from flask import current_app
import json
from superform import app
import requests

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

def get_channel_fields(form, chan):
    """
    :param form:
    :param chan:
    :return:
    """
    ictv_list = []
    end = False
    i = 1
    while not end:
        dictionary = {}
        if chan is None:
            title = form.get('ictv_' + str(i) + '_title')
            subtitle = form.get('ictv_' + str(i) + '_subtitle')
            text = form.get('ictv_' + str(i) + '_text')
            background_color = form.get('ictv_' + str(i) + '_background-color')
            duration = form.get('ictv_' + str(i) + '_duration')

            dictionary['ictv_' + str(i) + '_title'] = title
            dictionary['ictv_' + str(i) + '_subtitle'] = subtitle
            dictionary['ictv_' + str(i) + '_text'] = text
            dictionary['ictv_' + str(i) + '_background-color'] = background_color
            dictionary['ictv_' + str(i) + '_duration'] = duration
        else:
            title = form.get(chan + '_' + str(i) + '_title')
            subtitle = form.get(chan + '_' + str(i) + '_subtitle')
            text = form.get(chan + '_' + str(i) + '_text')
            background_color = form.get(chan + '_' + str(i) + '_background-color')
            duration = form.get(chan + '_' + str(i) + '_duration')

            dictionary[chan + '_' + str(i) + '_title'] = title
            dictionary[chan + '_' + str(i) + '_subtitle'] = subtitle
            dictionary[chan + '_' + str(i) + '_text'] = text
            dictionary[chan + '_' + str(i) + '_background-color'] = background_color
            dictionary[chan + '_' + str(i) + '_duration'] = duration
        if len(dictionary) > 0:
            ictv_list.append(dictionary)
        else:
            end = True
        i += 1
    extra = dict()
    extra['ictv_list'] = ictv_list
    return extra


def test_simple(requests_mock):
    with requests_mock.patch('/api/test') as patch:
        patch.returns = requests_mock.good('hello')
        response = requests.get('https://test.api/api/test')
        assert response.text == 'hello'
