from datetime import datetime
from functools import wraps
from flask import render_template, session, current_app
from superform.models import db, Post, Publishing
from sqlalchemy import or_, asc, desc

from superform.models import Authorization, Channel


def login_required(admin_required=False):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not session.get("logged_in", False) or (admin_required and not session.get("admin", False)):
                return render_template("403.html"), 403
            else:
                return f(*args, **kwargs)
        return decorated_function
    return decorator


def datetime_converter(stri):
    return datetime.strptime(stri, "%Y-%m-%d")

def str_converter(datet):
    return datetime.strftime(datet,"%Y-%m-%d")

def get_instance_from_module_path(module_p):
    module_p=module_p.replace(".","/")
    import importlib.util
    spec = importlib.util.spec_from_file_location("module.name", module_p+".py")
    foo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(foo)
    return foo

def get_modules_names(modules_keys):
    return [m.split('.')[2] for m in modules_keys]

def get_module_full_name(module_name):
    for m in current_app.config["PLUGINS"].keys():
        if(m.split('.')[2] == module_name):
            return m

"""
Just for the first version
"""
def add_q_filter_accessible_publications(query, user):
    #is our user an admin? -> return all publication ever published.
    if user.admin:
        return query

    #else: return all the posts user published || all the posts we can moderate
    post_user_wrote = db.session.query(Post).filter(Post.user_id == user.id)

    post_ids = [post.id for post in post_user_wrote]
    publications_query = Publishing.post_id.in_(post_ids)

    return query.filter(Publishing.post_id.in_(post_ids))

def add_q_filter_state(query, status):
    """
    status: either int (corresponing to requested status), or None (no status request)
    """
    if status != None:
        return query.filter(Publishing.state == status)
    else:
        return query

def add_q_filter_title_content(query, title, content):
    """
    Initial signature: query, title, content, words, split_words.
    If title == content, search for publishing that have either the title set to title, or the content set to content.
    Otherwise, filters for posts that contains exactly title(if present) and content(if present).
    """
    if title == content and title != None:
        """We search if the file contains the s"""
        return query.filter(or_(Publishing.title == title, Publishing.description.contains(content)))

    if title:
        query = query.filter(Publishing.title == title)
    if content:
        query = query.filter(Publishing.description.contains(content))

    return query

def add_q_order(query, is_asc, arg):
    """
    We can order by: date, author, channel
    @pre: is_asc either true/false/None, arg = channel/date.
    @post: order the query by is_asc?asc:desc of channel/date (defaults: desc, date)
    """

    known_arg  = {"channel": Publishing.channel_id, "date":Publishing.date_from}
    if is_asc:
        return query.order_by(asc(known_arg.get(arg, Publishing.date_from)))
    else:
        return query.order_by(desc(known_arg.get(arg, Publishing.date_from)))
