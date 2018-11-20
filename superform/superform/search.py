from flask import Blueprint, render_template
from superform.utils import login_required
from superform.models import db, Post, Publishing
from superform.users import get_moderate_channels_for_user

search_page = Blueprint('search', __name__)


@search_page.route('/search', methods=["GET", "POST"])
@login_required()
def search():
    return render_template('search.html', lol=1)


def query_maker(filter_parameter):
    """
    Function which makes a query to the DB to retrieve the publications corresponding to the filter parameter.

    :param filter_parameter: A dictionary containing the different filter parameters
    :return: The wanted query
    """
    print(db.session.query(Publishing).filter(filters(filter_parameter)).order_by(
        order_query(filter_parameter["order_by"], filter_parameter["is_asc"])))
    return db.session.query(Publishing).filter(filters(filter_parameter)).order_by(
        order_query(filter_parameter["order_by"], filter_parameter["is_asc"])).all()


def filters(filter_parameter):
    """
    A function which creates the filters (corresponding to the input filter_paremeter) to add to a query in order to
    retrieve certain publication.

    :param filter_parameter: a dictionary representing the different filter to apply
    :return: the list of publication according to the filter parameter
    """
    return filter_query_accessible_publications(filter_parameter["user"]) & filter_query_channel(
        filter_parameter["channels"]) & filter_query_status(filter_parameter["states"]) & filter_query_title_content(
        filter_parameter["search_in_title"], filter_parameter["search_in_content"], filter_parameter["searched_words"],
        filter_parameter["search_by_keyword"])


def filter_query_accessible_publications(user):
    """
    A function which returns the different publication permitted by an user.

    :param user: a User object representing the current user.
    :return: the filter parameters allowing user only seeing publishings he has haccess.
    """
    condition = (Publishing.post_id == None)
    if not user.admin:
        user_post = db.session.query(Post).filter(Post.user_id == user.user_id)
        for post in user_post:
            condition = condition | (Publishing.post_id == post.id)
        for chan in get_moderate_channels_for_user(user):
            condition = condition | (Publishing.channel_id == chan.id)
    else:
        condition = (Publishing.post_id != None)
    return condition


def filter_query_channel(channels):
    """
        A function which returns the different publications published in a particular channel

        :param channels: a list of channel_id
        :return: the filter parameters allowing to show publishings in the channels defined by the input channels
        """
    condition = (Publishing.post_id == None)
    for chan_id in channels:
        condition = condition | (Publishing.channel_id == chan_id)
    return condition


def filter_query_status(states):
    """
    A function which returns a filter allowing only publishings with certain state

    :param states: A list containing the states the publishings has to possess
    :return: a filter parameter allowing only publishings with a state defined by states
    """
    condition = (Publishing.post_id == None)
    for state in states:
        condition = condition | (Publishing.state == state)
    return condition


def filter_query_title_content(title, content, searched_words, split_words):
    """
    A function which returns a a filter allowing publishings with a particular content/title

    :param title: A boolean saying if we want to search in the title of the publication
    :param content: A boolean saying if we want to search in the title of the publication
    :param searched_words: A string representing what the title/content must contain
    :param split_words: If we want that the tile/content only have to have only one of the word in words
    :return: the filter to add to a query to filter publishings having the title/content corresponding to the inputs.
    """
    if split_words:
        condition = (Publishing.post_id == None)
        for word in searched_words.split():
            if title & content:
                condition = condition | Publishing.title.ilike(word) | Publishing.title.ilike(word + ' %') | Publishing.title.ilike('% '+word) | Publishing.title.ilike('% '+word+' %') | \
                            Publishing.description.ilike(word) | Publishing.description.ilike(word + ' %') | Publishing.description.ilike('% ' + word) | Publishing.description.ilike('% ' + word + ' %')
            elif title:
                condition = condition | Publishing.title.ilike(word) | Publishing.title.ilike(word + ' %') | Publishing.title.ilike('% '+word) | Publishing.title.ilike('% '+word+' %')
            else:
                condition = condition | Publishing.description.ilike(word) | Publishing.description.ilike(word + ' %') | Publishing.description.ilike('% ' + word) | Publishing.description.ilike('% ' + word + ' %')
        return condition
    else:
        if title & content:
            return Publishing.title.contains(searched_words) | Publishing.description.contains(searched_words)
        elif title:
            return Publishing.title.contains(searched_words)
        else:
            return Publishing.description.contains(searched_words)


def order_query(order_by, is_asc):
    """
    A function which returns the order parameter to order the publishings according to a parameter (and ascending/descending)

    :param order_by: the parameter corresponding to how the publishings will be sorted
    :param is_asc: True if we want to order in an ascending order, False if descending
    :return: the order parameter to display the publishings according to the inputs.
    """
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
