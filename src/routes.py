from flask import Blueprint
from src.controllers.user_controller import users
from src.controllers.main_controller import main
from src.controllers.blog_controller import blog
from flask import Blueprint

# api blueprint to be registered with application
api = Blueprint('api', __name__)
# register user with api blueprint
api.register_blueprint(users, url_prefix="/users")
# main navigation
mainNav = Blueprint('mainNav', __name__)
mainNav.register_blueprint(main, url_prefix="/")
mainNav.register_blueprint(blog, url_prefix="/blog/")
