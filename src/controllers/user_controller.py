from flask import request, Response, json, Blueprint, render_template
from src.models.models import Post, Assignment, Categorization, Comment, Profile, Role, Tag, User

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


# route for login api/users/signin
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
