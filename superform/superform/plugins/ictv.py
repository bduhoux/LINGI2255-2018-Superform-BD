from flask import current_app
import json
from superform import app
import requests
import requests_mock
from datetime import datetime
import time

FIELDS_UNAVAILABLE = ['Title', 'Description', 'Linkurl', 'Image']
CONFIG_FIELDS = []


def run(publishing):
    ictv_list = json.loads(publishing.extra)['ictv_list']

    title = publishing.title
    date_from = datetime.strptime(publishing.date_from.strip(), '%d-%M-%Y').timetuple()
    date_until = datetime.strptime(publishing.date_from.strip(), '%d-%M-%Y').timetuple()

    dictionary = {
        'name': title,
        'theme': "ictv",
        "validity": [
            int(time.mktime(date_from)),
            int(time.mktime(date_until))
        ]
    }

    response = requests.post('mock://ictv.com/capsules', dictionary)

    if response.status_code is not 201:
        response.raise_for_status()
        return

    location = response.headers['location']

    url_list = location.split('/')

    id_capsule = url_list[len(url_list) - 1]




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

adapter = requests_mock.Adapter()
session = requests.Session()
session.mount('mock', adapter)

adapter.register_uri('POST', 'mock://ictv.com/capsules', text='capsule created', status_code=201, headers={
    'location': 'mock://ictv.com/capsules/1'
})


@requests_mock.Mocker()
def create_slide(m, id_capsule, id_slide, dictionary):
    m.post('mock://ictv.com/capsules/' + id_capsule + '/slides', text='slide created', status_code=201, headers={
        'location': "mock://ictv.com/capsules/" + id_capsule + "/slides/" + id_slide
    })

    return requests.post('mock://ictv.com/capsules/' + id_capsule + '/slides', dictionary).status_code
