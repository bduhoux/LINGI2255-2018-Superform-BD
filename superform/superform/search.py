from flask import session, Blueprint, url_for, render_template
from superform.utils import login_required
from superform.models import db, User, Post, Publishing
from superform.users import get_moderate_channels_for_user, is_moderator

search_page = Blueprint('search', __name__)


@search_page.route('/search', methods=["GET", "POST"])
@login_required()
def search():
    return render_template('search.html', lol=1)


def query_maker(filter_parameter):
    return db.session.query(Publishing).filter(filters(filter_parameter)).order_by(
        order_query(filter_parameter["order_by"], filter_parameter["is_asc"])).all()


def filters(filter_parameter):
    """
    :param filter_parameter: a dictionary representing the different filter to apply
    :param publications: the list of publication
    :return: the list of publication according to the filter parameter
    """
    return filter_query_accessible_publications(filter_parameter["user"]) & \
           filter_query_channel(filter_parameter["channels"]) & \
           filter_query_status(filter_parameter["status"]) & \
           filter_query_title_content(filter_parameter["search_in_title"], filter_parameter["search_in_content"],
                                      filter_parameter["searched_words"])


def filter_query_accessible_publications(user):
    condition = (Publishing.post_id == None)
    if not user.admin:
        user_post = db.session.query(Post).filter(Post.user_id == user.user_id)
        for post in user_post:
            condition = condition | Publishing.post_id == post.id
        for chan in get_moderate_channels_for_user(user):
            condition = condition | Publishing.channel_id == chan.id
    else:
        condition = (Publishing.post_id != None)
    return condition


def filter_query_channel(channels):
    condition = (Publishing.post_id == None)
    for chan_id in channels:
        condition = condition | Publishing.channel_id == chan_id
    return condition


def filter_query_status(states):
    condition = (Publishing.post_id == None)
    for state in states:
        condition = condition | Publishing.state == state
    return condition


def filter_query_title_content(title, content, searched_words, split_words=False):
    if split_words:
        condition = (Publishing.post_id == None)
        for word in searched_words.split():
            if title & content:
                condition = condition | Publishing.title.ilike(word) | Publishing.content.ilike(word)
            elif title:
                condition = condition | Publishing.title.ilike(word)
            else:
                condition = condition | Publishing.content.ilike(word)
        return condition
    else:
        if title & content:
            return Publishing.title.contains(searched_words) | Publishing.content.contains(searched_words)
        elif title:
            return Publishing.title.contains(searched_words)
        else:
            return Publishing.content.contains(searched_words)


def order_query(order_by, is_asc):
    fil = {
        "post_id": Publishing.post_id,
        "channel_id": Publishing.channel_id,
        "state": Publishing.state,
        "title": Publishing.title,
        "description": Publishing.description,
        "link_url": Publishing.link_url,
        "image__url": Publishing.image_url,
        "date_from": Publishing.date_from,
        "date_until": Publishing.date_until,
    }
    if is_asc:
        return fil[order_by]
    else:
        return fil[order_by].desc()
