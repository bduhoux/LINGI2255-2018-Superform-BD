from datetime import datetime
from functools import wraps
from flask import render_template, session, current_app
from models import db, Post, Publishing

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

    print("We wrote: ", post_user_wrote);

    post_ids = [post.id for post in post_user_wrote]
    publications_query = Publishing.post_id.in_(post_ids)

    return publications_query

def add_q_filter_channel(query, status):
    """ Query will be a tuple of filters."""

    """
    example of use:
     query = '((),)
     query = add_q_filter_accessible_publications(query, user)
     query = add_q_filter_channel(query, status)
     ...
     bd.session.query(Publishing).filter(query)
    """
    return query + Publishing.state == status

def add_q_filter_title_content(query, title, content, words, split_words=False):
    "still need to test this"

    return query + or_(Publishing.title == title, Publishing.description.contains(content))

def add_q_order(query, asc, arg):
    return query


"""
def search(..., ...):
    query = "SELECT * FROM PUBLICATIONS WHERE ";
    add_q_filter_accessbile_publications(query, current_user);
    ...
    db.apply_query(query);
    ->voir comment combiner: , vs &.

"""
