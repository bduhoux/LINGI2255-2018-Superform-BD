from flask import Blueprint, url_for, request, redirect, render_template, session

from superform.utils import login_required, datetime_converter, str_converter
from superform.models import db, Publishing, Channel
from superform.plugins.facebook import fb_token

pub_page = Blueprint('publishings', __name__)
@pub_page.route('/moderate/<int:id>/<string:idc>',methods=["GET","POST"])
@login_required()
def moderate_publishing(id,idc):
    pub = db.session.query(Publishing).filter(Publishing.post_id==id,Publishing.channel_id==idc).first()
    pub.date_from = str_converter(pub.date_from)
    pub.date_until = str_converter(pub.date_until)
    if request.method=="GET": # quand on appuye sur moderate
        # session["facebook_running"] = False # marche car bouton s'affiche pas, à enlever plus tard
        session["facebook_running"] = True  # à enlever plus tard qd ci dessous marche



        # todo
        """
        print("0")
        print(pub.channel_id) # affiche bien "fb"
        print("1")
        v = db.session.query(Channel).filter(Channel.name == pub.channel_id).first() # PQ marche pas????!!!!! si ça ça marche, cacher bouton login fb marche 
        print(v.module)
        if v.module == "superform.plugins.facebook":
            session["facebook_running"] = True
        else:
            session["facebook_running"] = False
        """
        return render_template('moderate_post.html', pub=pub)
    else: # quand on appuye sur publish
        if pub.channel_id == "fb":
            print(fb_token)
            session["facebook_running"] = True
            if fb_token == 0: # pq reste à 0 quand délogé puis relogé après??? todo
                return redirect(url_for('publishings.moderate_publishing',id=id,idc=idc))
        else:
            session["facebook_running"] = False
        print("published")
        pub.title = request.form.get('titlepost')
        pub.description = request.form.get('descrpost')
        pub.link_url = request.form.get('linkurlpost')
        pub.image_url = request.form.get('imagepost')
        pub.date_from = datetime_converter(request.form.get('datefrompost'))
        pub.date_until = datetime_converter(request.form.get('dateuntilpost'))
        # state is shared & validated
        pub.state = 1
        db.session.commit()
        # running the plugin here
        c = db.session.query(Channel).filter(Channel.name == pub.channel_id).first()
        plugin_name = c.module
        c_conf = c.config
        from importlib import import_module
        plugin = import_module(plugin_name)
        plugin.run(pub, c_conf)
        return redirect(url_for('index'))


