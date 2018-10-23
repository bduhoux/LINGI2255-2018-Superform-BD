from superform.utils import datetime_converter, str_converter, get_module_full_name
from superform import app, db, Post, User
from superform.models import Authorization, Channel
from superform.users import is_moderator, get_moderate_channels_for_user, channels_available_for_user
from superform.feed import rss_feed
from superform.models import db, Publishing, Channel


def test_get_module_rss():
    module_name = "rss"
    m = get_module_full_name(module_name)
    assert m == "superform.plugins.rss"


def test_channel_rss():
    """
    For the sake of this test, you must erase all the channels with rss
    :return:
    """
    channel = Channel.query.filter_by(
        module='superform.plugins.rss'
    ).first()

    assert channel is None

    channel = Channel(name="test", module=get_module_full_name("rss"), config="{}")
    db.session.add(channel)

    channel = Channel.query.filter_by(
        module='superform.plugins.rss'
    ).first()

    assert channel is not None

    assert channel.name == 'test'
