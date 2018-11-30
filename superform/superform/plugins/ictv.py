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
            background_color = form.get('ictv_' + str(i) + '_background')
            duration = form.get('ictv_' + str(i) + '_duration')
            logo = form.get('ictv_' + str(i) + '_logo')
            image = form.get('ictv_' + str(i) + '_image')

            dictionary['title-1'] = {'text': title}
            dictionary['subtitle-1'] = {'text': subtitle}
            dictionary['text-1'] = {'text': text}
            dictionary['background-1'] = {'color': background_color}
            dictionary['duration'] = duration
            dictionary['logo-1'] = {'src': logo}
            dictionary['image-1'] = {'src': image}

        else:
            title = form.get(chan + '_' + str(i) + '_title')
            subtitle = form.get(chan + '_' + str(i) + '_subtitle')
            text = form.get(chan + '_' + str(i) + '_text')
            background_color = form.get(chan + '_' + str(i) + '_background')
            duration = form.get(chan + '_' + str(i) + '_duration')
            logo = form.get(chan + '_' + str(i) + '_logo')
            image = form.get(chan + '_' + str(i) + '_image')

            dictionary['title-1'] = {'text': title}
            dictionary['subtitle-1'] = {'text': subtitle}
            dictionary['text-1'] = {'text': text}
            dictionary['background-1'] = {'color': background_color}
            dictionary['duration'] = duration
            dictionary['logo-1'] = {'src': logo}
            dictionary['image-1'] = {'src': image}

        if title is not None:
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
