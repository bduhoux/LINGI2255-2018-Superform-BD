from datetime import datetime

from flask import Blueprint, url_for, request, redirect, render_template, flash, session
from superform.utils import login_required
from superform.models import db, Post, Publishing, User, Channel
from superform.users import get_moderate_channels_for_user, channels_available_for_user

search_page = Blueprint('search', __name__)


@search_page.route('/search', methods=["GET", "POST"])
@login_required()
def search():
    user_id = session.get('user_id', '') if session.get('logged_in', False) else -1
    l_chan = channels_available_for_user(user_id)
    if request.method == 'GET':
        return render_template('search.html', l_chan=l_chan, post=False)
    else:
        user = User.query.get(user_id) if session.get("logged_in", False) else None
        print(user)
        pattern = request.form.get('search_word')
        chan = request.form.getlist('search_chan')
        status = request.form.getlist('post_status')
        loc = request.form.getlist('search_loc')
        date_from = request.form.get('date_from')
        date_until = request.form.get('date_until')
        search_type = request.form.get('search_type') == 'keyword'
        search_table = request.form.get('search_table')
        print(search_table)
        filter_parameter = make_filter_parameter(user_id, pattern, chan, status, loc, date_from, date_until,
                                                 search_type, search_table)
        search_result = query_maker(filter_parameter)
        return render_template('search.html', l_chan=l_chan, publishing=search_result, post=True,
                               moderate_channel=[x.id for x in get_moderate_channels_for_user(user)],
                               search_table=search_table, user_id=user.id)


def make_filter_parameter(user_id, pattern, channels, post_status, search_location, date_from=False, date_until=False,
                          search_by_keyword=False, search_table="Publishing"):
    user = User.query.get(user_id) if session.get("logged_in", False) else None
    return {
        'user': user,
        'channels': channels,
        'states': post_status,
        'search_in_title': 'title' in search_location,
        'search_in_content': 'description' in search_location,
        'searched_words': pattern,
        'search_by_keyword': search_by_keyword,
        'date_from': date_from,
        'date_until': date_until,
        'search_table': Post if search_table == "Post" else Publishing
    }


def query_maker(filter_parameter):
    """
    Function which makes a query to the DB to retrieve the publications corresponding to the filter parameter.

    :param filter_parameter: A dictionary containing the different filter parameters
    :return: The wanted query
    """
    #print(db.session.query(filter_parameter["search_table"]).filter(filters(filter_parameter)))
    return db.session.query(filter_parameter["search_table"]).filter(filters(filter_parameter)).all()


def filters(filter_parameter):
    """
    A function which creates the filters (corresponding to the input filter_paremeter) to add to a query in order to
    retrieve certain publication.

    :param filter_parameter: a dictionary representing the different filter to apply
    :return: the list of publication according to the filter para#dmeter
    """
    return filter_query_accessible_publications(filter_parameter["user"], filter_parameter["search_table"]) \
                       & filter_query_channel(filter_parameter["channels"], filter_parameter["search_table"]) \
                       & filter_query_status(filter_parameter["states"], filter_parameter["search_table"]) \
                       & filter_query_title_content(filter_parameter.get("search_in_title", None),
                                                    filter_parameter.get("search_in_content", None),
                                                    filter_parameter.get("searched_words", None),
                                                    filter_parameter.get("search_by_keyword", None),
                                                    filter_parameter["search_table"]) \
                       & filter_date(filter_parameter.get("date_from", None), filter_parameter.get("date_until", None),
                             filter_parameter["search_table"])


def filter_query_accessible_publications(user, table):
    """
    A function which returns the different publication permitted by an user.

    :param user: a User object representing the current user.
    :return: the filter parameters allowing user only seeing publishings he has haccess.
    """
    condition = (table.post_id == None) if table == Publishing else (table.id == None)
    user_post = db.session.query(Post).filter(Post.user_id == user.id)
    for post in user_post:
        condition = condition | (table.post_id == post.id) if table == Publishing else condition | (
                table.id == post.id)

    if table == Publishing:
        for chan in get_moderate_channels_for_user(user):
            condition = condition | (table.channel_id == chan.id)


    return condition


def filter_query_channel(channels, table):
    """
        A function which returns the different publications published in a particular channel

        :param channels: a list of channel_id
        :return: the filter parameters allowing to show publishings in the channels defined by the input channels
        """
    condition = (table.post_id == None) if table == Publishing else (table.id == None)
    if table == Post:
        return (table.id != None)
    if not channels:
        return (table.post_id != None)
    for chan_id in channels:
        condition = condition | (table.channel_id == chan_id)
    return condition


def filter_query_status(states, table):
    """
    A function which returns a filter allowing only publishings with certain state

    :param states: A list containing the states the tables has to possess
    :return: a filter parameter allowing only publishings with a state defined by states
    """
    if table == Post:
        return (table.id != None)
    if not states:
        return (table.post_id != None)
    condition = (table.post_id == None)
    for state in states:
        condition = condition | (table.state == state)
    return condition


def filter_query_title_content(title, content, searched_words, split_words,table):
    """
    A function which returns a a filter allowing publishings with a particular content/title

    :param title: A boolean saying if we want to search in the title of the publication
    :param content: A boolean saying if we want to search in the title of the publication
    :param searched_words: A string representing what the title/content must contain
    :param split_words: If we want that the tile/content only have to have only one of the word in words
    :return: the filter to add to a query to filter publishings having the title/content corresponding to the inputs.
    """
    if split_words:
        if (searched_words == '') | (searched_words == ' ') | (searched_words is None):
            return (table.post_id != None) if table == Publishing else (table.id != None)
        condition = (table.post_id == None)
        for word in searched_words.split():
            if title & content:
                condition = condition | table.title.contains(word) | table.description.contains(word)
            elif title:
                condition = condition | table.title.contains(word)
            else:
                condition = condition | table.description.contains(word)
        return condition
    elif not split_words:
        if title & content:
            return table.title.contains(searched_words) | table.description.contains(searched_words)
        elif title:
            return table.title.contains(searched_words)
        else:
            return table.description.contains(searched_words)
    else:
        return table.post_id != None  # Return true means all publishings are accepted


def filter_date(date_from, date_until, table):
    """
    Return a filter parameter allowing only Publishing from a particular and/or to a particular date (if none of them
    are expressed, there will be no filtering)

    :param date_from: if not None, filter only publishing posted after a particular date
    :param date_until: if not Node, filter only publishing posted before a particular date
    :return: A binary Expression filtering the requested publishings by date
    """
    condition = (table.post_id != None) if table == Publishing else (table.id != None)
    if date_from:
        date = datetime.strptime(date_from, '%Y-%m-%d')
        condition = condition & (table.date_from >= date)
    if date_until:
        date = datetime.strptime(date_until, '%Y-%m-%d')
        condition = condition & (table.date_until <= date)
    return condition
