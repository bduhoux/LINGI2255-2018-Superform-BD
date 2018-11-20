
from flask import session
from superform.models import db, User, Post, Publishing
from  superform.users import get_moderate_channels_for_user, is_moderator


def get_accessible_publications_of_user(user):
    """
    Defining publication access as such for a user:
        -all publication published on superform for a Admin
        -all publication published on moderated channels for a Moderator
        -all publication written for a Writer
    Returns an empty list if user_id is invalid;
    otherwise returns all accesible post for matching user.
    """

    #is our user an admin? -> return all publication ever published.
    if user.admin:
        return db.session.query(Publishing).all()

    #else: return all the posts user published || all the posts we can moderate
    post_user_wrote = db.session.query(Post).filter(Post.user_id == user.user_id)
    publications_user_wrote = (db.session.query(Publishing).filter(Publishing.post_id == post.id) for post in post_user_wrote)

    flattened_publication = [y for x in publications_user_wrote for y in x]

    if is_moderator(user):
        chans = get_moderate_channels_for_user(user)
        pubs_per_chan = (db.session.query(Publishing).filter((Publishing.channel_id == c.id) & (Publishing.state == 0)) for c in chans)
        flattened_publication.append( [y for x in pubs_per_chan for y in x])

    return flattened_publication


"""
remarque:

    db.session.query(Publishing).filter(f1(c), f2(...)...)
    def f1(c):
        return (Publishing.channel_Id == c.id) & (Publishing.state ==0)

    ->accumuller tout les filters, puis les grouper.
"""