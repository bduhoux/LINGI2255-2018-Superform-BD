import json
import twitter
from flask import Blueprint, url_for, request, redirect, render_template, session

from superform.utils import login_required, datetime_converter, str_converter
from superform.models import db, Publishing, Channel

pub_page = Blueprint('publishings', __name__)


@pub_page.route('/moderate/<int:id>/<string:idc>', methods=["GET", "POST"])
@login_required()
def moderate_publishing(id, idc):
    pub = db.session.query(Publishing).filter(Publishing.post_id == id, Publishing.channel_id == idc).first()
    chan = db.session.query(Channel).filter(Channel.id == idc).first()
    pub.date_from = str_converter(pub.date_from)
    pub.date_until = str_converter(pub.date_until)
    if request.method == "GET":
        if pub.extra is not None:
            pub.extra = json.loads(pub.extra)
        return render_template('moderate_post.html', pub=pub, chan=chan)
    else:
        pub.title = request.form.get('titlepost')
        pub.description = request.form.get('descrpost')
        pub.link_url = request.form.get('linkurlpost')
        pub.image_url = request.form.get('imagepost')
        pub.date_from = datetime_converter(request.form.get('datefrompost'))
        pub.date_until = datetime_converter(request.form.get('dateuntilpost'))
        extra = dict()
        if chan.module == "superform.plugins.Twitter":
            extra['truncated'] = request.form.get("truncate") == "Truncate"
            pub.extra = json.dumps(extra)
    #state is shared & validated
        pub.state = 1
        db.session.commit()
        # running the plugin here
        c = db.session.query(Channel).filter(Channel.id == pub.channel_id).first()
        plugin_name = c.module
        c_conf = c.config
        from importlib import import_module
        plugin = import_module(plugin_name)
        try:
            plugin.run(pub, c_conf)
        except KeyError:
            return render_template('error.html', message="The channel is not configured. Configure the channel and try again")
        except twitter.error.TwitterError:
            pub.state = 1
            db.session.commit()
            return render_template('error.html', message="An error occured: one or more of your tweet(s) haven't been posted.\n Please make sure to not duplicate your tweets")

        # state is shared & validated
        pub.state = 1
        db.session.commit()

        return redirect(url_for('index'))
