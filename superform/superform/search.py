from flask import session, Blueprint, url_for, render_template
from superform.utils import login_required
from superform.models import db, User, Post, Publishing
from superform.users import get_moderate_channels_for_user, is_moderator

search_page = Blueprint('search', __name__)


@search_page.route('/search', methods=["GET", "POST"])
@login_required()
def search():
    return render_template('search.html', lol=1)


def filter_query_accessible_publication(user):
    """
    Defining publication access as such for a user:
        -all publication published on superform for a Admin
        -all publication published on moderated channels for a Moderator
        -all publication written for a Writer
    Returns an empty list if user_id is invalid;
    otherwise returns all accesible post for matching user.
    """

    # is our user an admin? -> return all publication ever published.
    if user.admin:
        return db.session.query(Publishing).all()

    # else: return all the posts user published || all the posts we can moderate
    post_user_wrote = db.session.query(Post).filter(Post.user_id == user.user_id)
    publications_user_wrote = (db.session.query(Publishing).filter(Publishing.post_id == post.id) for post in
                               post_user_wrote)

    flattened_publication = [y for x in publications_user_wrote for y in x]

    if is_moderator(user):
        chans = get_moderate_channels_for_user(user)
        pubs_per_chan = (db.session.query(Publishing).filter((Publishing.channel_id == c.id))
                         # & (Publishing.state == 0))
                         for c in chans)
        flattened_publication.append([y for x in pubs_per_chan for y in x])

    return flattened_publication


def filter_query_accessible_publications(user):
    l = None
    if not user.admin:
        a = db.session.query(Post).filter(Post.user_id == user.user_id)
        for post in a:
            if l :
                l = l | Publishing.post_id == post.id
            else :
                l = Publishing.post_id == post.id
        if is_moderator(user):
            for c in get_moderate_channels_for_user(user):
                if l:
                    l = l | Publishing.channel_id == c.id
                else:
                    l = Publishing.channel_id == c.id
    return l


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


def filter_query_channel(channels):
    l = None
    for cha in channels:
        if l:
            l = l | Publishing.channel_id == cha
        else:
            l = Publishing.channel_id == cha
    return l


def filter_query_status(status):
    l = None
    for cha in status:
        if l:
            l = l | Publishing.state == cha
        else:
            l = Publishing.state == cha
    return l


def filter_query_title_content(title, content, words, split_words=False):
    l = None
    if split_words:
        for mot in words :
            if title & content:
                if l :
                    l = l |Publishing.title.ilike(mot) | Publishing.content.ilike(mot)
                else:
                    l = Publishing.title.ilike(mot) | Publishing.content.ilike(mot)
            elif title:
                if l :
                    l = l |Publishing.title.ilike(mot) | Publishing.content.ilike(mot)
                else:
                    l = Publishing.title.ilike(mot) | Publishing.content.ilike(mot)
            else:
                if l :
                    l = l |Publishing.title.ilike(mot) | Publishing.content.ilike(mot)
                else:
                    l = Publishing.title.ilike(mot) | Publishing.content.ilike(mot)
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
