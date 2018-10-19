from superform.utils import datetime_converter, str_converter, get_module_full_name
from superform import app, db, Post, User
from superform.models import Authorization, Channel
from superform.users import  is_moderator, get_moderate_channels_for_user,channels_available_for_user
from superform.feed import rss_feed


def test_get_module_rss():
    module_name = "rss"
    m = get_module_full_name(module_name)
    assert m == "superform.plugins.rss"
