from flask import Blueprint, current_app, url_for, request, make_response, redirect, session, render_template

from superform.utils import login_required, get_instance_from_module_path, get_modules_names, get_module_full_name
from superform.models import db, Channel
from datetime import datetime
import ast

# For the archival module :
from archival_module import configure_job, FREQUENCIES

channels_page = Blueprint('channels', __name__)


@channels_page.route("/channels", methods=['GET', 'POST'])
@login_required(admin_required=True)
def channel_list():
    if request.method == "POST":
        action = request.form.get('@action', '')
        if action == "new":
            name = request.form.get('name')
            module = request.form.get('module')
            if module in get_modules_names(current_app.config["PLUGINS"].keys()):
                archival_date = datetime(2018, 1, 1, 0, 0)
                channel = Channel(name=name, module=get_module_full_name(module), config="{}",
                                  archival_frequency=2, archival_date=archival_date)
                db.session.add(channel)
                db.session.commit()
        elif action == "delete":
            channel_id = request.form.get("id")
            channel = Channel.query.get(channel_id)
            if channel:
                db.session.delete(channel)
                db.session.commit()
        elif action == "edit":
            channel_id = request.form.get("id")
            channel = Channel.query.get(channel_id)
            name = request.form.get('name')
            channel.name = name
            db.session.commit()

    channels = Channel.query.all()
    return render_template("channels.html", channels=channels,
                           modules=get_modules_names(current_app.config["PLUGINS"].keys()))


@channels_page.route("/configure/<int:id>", methods=['GET', 'POST'])
@login_required(admin_required=True)
def configure_channel(id):
    c = Channel.query.get(id)
    m = c.module
    clas = get_instance_from_module_path(m)
    config_fields = clas.CONFIG_FIELDS

    if request.method == 'GET':
        if (c.config is not ""):
            d = ast.literal_eval(c.config)
            setattr(c, "config_dict", d)
        return render_template("channel_configure.html", channel=c, config_fields=config_fields,
                               archival_f_dict=FREQUENCIES, archival_f=c.archival_frequency, archival_d=c.archival_date)
    str_conf = "{"
    cfield = 0
    for field in config_fields:
        if cfield > 0:
            str_conf += ","
        str_conf += "\"" + field + "\" : \"" + request.form.get(field) + "\""
        cfield += 1
    str_conf += "}"
    c.config = str_conf
    # Archival Module :
    arch_config = configure_job(id, request.form)
    if arch_config:
        c.archival_frequency = arch_config[0]
        if arch_config[0] != -1:
            c.archival_date = arch_config[1]
    # End of Archival Module
    db.session.commit()
    return redirect(url_for('channels.channel_list'))
