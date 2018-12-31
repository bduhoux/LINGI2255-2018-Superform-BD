from flask import Flask, render_template, session
import pkgutil
import importlib

import superform.plugins
from superform.publishings import pub_page
from superform.models import db, User, Post, Publishing
from superform.authentication import authentication_page
from superform.authorizations import authorizations_page
from superform.channels import channels_page
from superform.posts import posts_page
from superform.delete import delete_page
from superform.feed import feed_page
from superform.users import get_moderate_channels_for_user, is_moderator
from superform.plugins.facebook import facebook_plugin
from superform.search import search_page
from superform.archival_module import archival_page, start_jobs_from_db


def create_app(testing = False):
    app = Flask(__name__)
    app.config.from_json("config.json")

    # Register blueprints
    app.register_blueprint(authentication_page)
    app.register_blueprint(authorizations_page)
    app.register_blueprint(search_page)
    app.register_blueprint(channels_page)
    app.register_blueprint(posts_page)
    app.register_blueprint(pub_page)
    app.register_blueprint(feed_page)
    app.register_blueprint(archival_page)

    app.register_blueprint(delete_page)
    app.register_blueprint(facebook_plugin)
    print(app.config["SQLALCHEMY_DATABASE_URI"])

    if testing:
        app.config['TESTING'] = True
    # Init dbs
    db.init_app(app)

    # List available channels in config
    app.config["PLUGINS"] = {
        name: importlib.import_module(name)
        for finder, name, ispkg
        in pkgutil.iter_modules(superform.plugins.__path__, superform.plugins.__name__ + ".")
    }

    @app.route('/')
    def index():
        user = User.query.get(session.get("user_id", "")) if session.get("logged_in", False) else None
        posts = []
        flattened_list_pubs = []
        if user is not None:
            setattr(user, 'is_mod', is_moderator(user))
            posts = db.session.query(Post).filter(Post.user_id == session.get("user_id", ""))
            chans = get_moderate_channels_for_user(user)
            pubs_per_chan = (
            db.session.query(Publishing).filter((Publishing.channel_id == c.id) & (Publishing.state == 0)) for c in
            chans)
            flattened_list_pubs = [y for x in pubs_per_chan for y in x]

        return render_template("index.html", user=user, posts=posts, publishings=flattened_list_pubs)

    @app.errorhandler(403)
    def forbidden(error):
        return render_template('403.html'), 403

    @app.errorhandler(404)
    def notfound(error):
        return render_template('404.html'), 404
    return app

app = create_app()

if __name__ == '__main__':
    app.run()

    # Archival Module : (start all jobs)
    start_jobs_from_db()
