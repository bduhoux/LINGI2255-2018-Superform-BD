from functools import wraps
from flask import Blueprint, current_app, url_for, request, make_response, redirect, session, render_template
from flask_sqlalchemy import SQLAlchemy

from onelogin.saml2.auth import OneLogin_Saml2_Auth
from onelogin.saml2.utils import OneLogin_Saml2_Utils

from superform.models import User

auth_page = Blueprint('auth', __name__)
db = SQLAlchemy()


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("logged_in", False):
            return render_template("403.html"), 403
        return f(*args, **kwargs)
    return decorated_function


def prepare_saml_request(request):
    current_app.config["SAML"]["sp"]["assertionConsumerService"]["url"] = url_for("auth.callback", _external=True)
    return {
        'https': 'on' if request.scheme == 'https' else 'off',
        'http_host': request.host,
        'server_port': request.environ["SERVER_PORT"],
        'script_name': request.path,
        'get_data': request.args.copy(),
        'post_data': request.form.copy(),
        'query_string': request.query_string
    }


@auth_page.route('/metadata')
def metadata():
    auth = OneLogin_Saml2_Auth(prepare_saml_request(request), current_app.config["SAML"])
    metadata = auth.get_settings().get_sp_metadata()
    errors = auth.get_settings().validate_metadata(metadata)

    if len(errors) == 0:
        resp = make_response(metadata, 200)
        resp.headers['Content-Type'] = 'text/xml'
    else:
        resp = make_response(', '.join(errors), 500)
    return resp


@auth_page.route("/callback", methods=['GET', 'POST'])
def callback():
    auth = OneLogin_Saml2_Auth(prepare_saml_request(request), current_app.config["SAML"])
    auth.process_response()
    errors = auth.get_errors()
    if len(errors) == 0:
        auth_attrs = auth.get_attributes()
        mappings = current_app.config["SAML"]["attributes"]
        attrs = {key: auth_attrs[mapping][0] for key, mapping in mappings.items()}

        user = User.query.get(attrs["uid"])
        if not user:
            user = User(id=attrs["uid"], name=attrs["sn"], first_name=attrs["givenName"], email=attrs["email"])
            db.session.add(user)
            db.session.commit()

        session["logged_in"] = True
        session["id"] = user.id
        session["first_name"] = user.first_name
        session["name"] = user.name
        session["email"] = user.email

        # Redirect to desired url
        self_url = OneLogin_Saml2_Utils.get_self_url(prepare_saml_request(request))
        if 'RelayState' in request.form and self_url != request.form['RelayState']:
            return redirect(auth.redirect_to(request.form['RelayState']))
    else:
        return make_response(", ".join(errors), 500)

    return make_response("saml_acs_error", 500)


@auth_page.route('/login')
def login():
    auth = OneLogin_Saml2_Auth(prepare_saml_request(request), current_app.config["SAML"])
    return redirect(auth.login(url_for("index", _external=True)))


@auth_page.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("index"))