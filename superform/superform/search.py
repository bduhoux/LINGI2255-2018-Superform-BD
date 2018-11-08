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
    query = db.session.query(Publishing).filter(filters(filter_parameter))
    order_query(query, filter_parameter["asc"], filter_parameter["arg"])
    return query


def filters(filter_parameter):
    """
    :param filter_parameter: a dictionary representing the different filter to apply
    :param publications: the list of publication
    :return: the list of publication according to the filter parameter
    """
    return filter_query_accessible_publications(filter_parameter["user"]) & \
           filter_query_channel(filter_parameter["channel"]) & \
           filter_query_status(filter_parameter["status"]) & \
           filter_query_title_content(filter_parameter["title"], filter_parameter["content"],
                                      filter_parameter["words"])

def filter_query_accessible_publications(user):
    l = (Publishing.post_id == None)
    if not user.admin:
        a = db.session.query(Post).filter(Post.user_id == user.user_id)
        for post in a:
            l = l | Publishing.post_id == post.id
        if is_moderator(user):
            for c in get_moderate_channels_for_user(user):
                l = l | Publishing.channel_id == c.i
    return l


def filter_query_channel(channels):
    l = (Publishing.post_id == None)
    for cha in channels:
        l = l | Publishing.channel_id == cha
    return l


def filter_query_status(status):
    l = (Publishing.post_id == None)
    for cha in status:
        l = l | Publishing.state == cha
    return l


def filter_query_title_content(title, content, words, split_words=False):
    if split_words:
        l = (Publishing.post_id == None)
        for mot in words:
            if title & content:
                l = l | Publishing.title.ilike(mot) | Publishing.content.ilike(mot)
            elif title:
                l = l | Publishing.title.ilike(mot) | Publishing.content.ilike(mot)
            else:
                l = l | Publishing.title.ilike(mot) | Publishing.content.ilike(mot)
        return l
    else:
        if title & content:
            return Publishing.title.contains(words) | Publishing.content.contains(words)
        elif title:
            return Publishing.title.contains(words)
        else:
            return Publishing.content.contains(words)


def order_query(asc, arg, query):
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
    for term in arg:
        if asc:
            query.order(fil[term])
        else:
            query.order(fil[term].desc())


"""
remarque:

    db.session.query(Publishing).filter(f1(c), f2(...)...)
    def f1(c):
        return (Publishing.channel_Id == c.id) & (Publishing.state ==0)

    ->accumuller tout les filters, puis les grouper.
"""
