from flask import request, Response, json, Blueprint, render_template
from src.models.models import Post, Assignment, Categorization, Comment, Profile, Role, Tag, User
from src.controllers.errors import ApiException, check_error
import logging
import re

logger = logging.getLogger(__name__)

# from https://github.com/pallets-eco/flask-security/blob/main/examples/unified_signin/client/client.py


def register(server_url, session, email, password):
    # Register new email with password
    # Use the backdoor to grab confirmation email and confirm.

    resp = session.post(
        f"{server_url}/register",
        json={"email": email, "password": password},
    )
    check_error(resp)

    resp = session.get(f"{server_url}/api/popmail")
    if resp.status_code != 200:
        raise ApiException("popmail error", resp.status_code)

    jbody = resp.json()

    # Parse for link
    matcher = re.match(
        r".*(http://[^\s*]*).*", jbody["mail"], re.IGNORECASE | re.DOTALL
    )
    magic_link = matcher.group(1)

    # Note this simulates someone clicking on the email link - no point in claiming
    # this is json.
    resp = session.get(magic_link, allow_redirects=False)
    assert resp.status_code == 302


def ussetup(server_url, session, password, phone):
    # unified sign in - setup sms with a phone number
    # Use the backdoor to grab verification SMS.

    # reset freshness to show how that would work
    resp = session.get(f"{server_url}/api/resetfresh")

    csrf_token = session.cookies["XSRF-TOKEN"]
    resp = session.post(
        f"{server_url}/us-setup",
        json={"chosen_method": "us_phone_number", "phone": phone},
        headers={"X-XSRF-Token": csrf_token},
    )

    # this should be a 401 reauth required
    assert resp.status_code == 401
    jbody = resp.json()
    assert jbody["response"]["reauth_required"]

    # re-verify
    resp = session.post(
        f"{server_url}/us-verify",
        json={"passcode": password},
        headers={"X-XSRF-Token": csrf_token},
    )
    assert resp.status_code == 200

    # try again
    resp = session.post(
        f"{server_url}/us-setup",
        json={"chosen_method": "sms", "phone": phone},
        headers={"X-XSRF-Token": csrf_token},
    )
    check_error(resp)
    jbody = resp.json()
    state = jbody["response"]["state"]

    resp = session.get(f"{server_url}/api/popsms")
    if resp.status_code != 200:
        raise ApiException("popsms error", resp.status_code)

    jbody = resp.json()
    code = jbody["sms"].split()[-1].strip(".")
    resp = session.post(
        f"{server_url}/us-setup/{state}",
        json={"passcode": code},
        headers={"X-XSRF-Token": csrf_token},
    )
    check_error(resp)


def sms_signin(server_url, session, username, phone):
    # Sign in using SMS code.
    session.post(
        f"{server_url}/us-signin/send-code",
        json={"identity": username, "chosen_method": "sms"},
    )

    # Fetch code via test API
    resp = session.get(f"{server_url}/api/popsms")
    if resp.status_code != 200:
        raise ApiException("popsms error", resp.status_code)

    jbody = resp.json()
    code = jbody["sms"].split()[-1].strip(".")
    resp = session.post(
        f"{server_url}/us-signin",
        json={"identity": username, "passcode": code},
    )
    check_error(resp)


# user controller blueprint to be registered with api blueprint
users = Blueprint("users", __name__)


@users.route('/')
def users_list():
    user_list = User.query.all()

    return render_template('users/userlist.html.jinja', users=user_list)


@users.route('/profile/<int:id>')
def user_profile(id):
    requested_user = User.query.get_or_404(id)
    return render_template('users/userprofile.html.jinja', user=requested_user)


@users.route('/profile/<string:name>')
def user_profile_by_name(name):
    requested_user = User.query.filter_by(display_name=name).first_or_404()
    return render_template('users/userprofile.html.jinja', user=requested_user)


# @users.route('/login')
# def login_page():
#     return render_template('users/login.html.jinja')


# @users.route('/register')
# def register():
#     return render_template('users/register.html.jinja')


@users.route('/signin', methods=["GET", "POST"])
def handle_login():
    return Response(
        response=json.dumps({'status': "success"}),
        status=200,
        mimetype='application/json'
    )

# route for login api/users/signup


@users.route('/signup', methods=["GET", "POST"])
def handle_signup():
    return Response(
        response=json.dumps({'status': "success"}),
        status=200,
        mimetype='application/json'
    )
