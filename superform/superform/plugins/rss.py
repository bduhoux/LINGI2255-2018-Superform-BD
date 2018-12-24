from flask import current_app
import json

FIELDS_UNAVAILABLE = []
CONFIG_FIELDS = []


def run(publishing, channel_config):
    # We don't need to do anything here. We'll just query the database when a
    # user requests the RSS feed.
    pass
