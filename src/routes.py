from flask import Blueprint
from src.controllers.user_controller import users
from src.controllers.main_controller import main

# api blueprint to be registered with application
api = Blueprint('api', __name__)
# register user with api blueprint
api.register_blueprint(users, url_prefix="/users")



# main navigation
mainNav = Blueprint('mainNav', __name__)
mainNav.register_blueprint(main, url_prefix="/")