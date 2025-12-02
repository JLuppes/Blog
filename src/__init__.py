from flask import Flask
import os
from src.config.config import Config
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_bootstrap import Bootstrap5
from flask_wtf import CSRFProtect
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_security import (
    Security,
    SmsSenderFactory,
    SmsSenderBaseClass,
    uia_phone_mapper,
    uia_email_mapper,
)
from flask_babel import Babel
from src.models.models import db, user_datastore

# loading environment variables
load_dotenv()


class CaptureMail:
    # A hack Mail service that simply captures what would be sent.
    def __init__(self, app):
        app.extensions["mail"] = self
        self.sent = list()

    def send(self, msg):
        self.sent.append(msg.body)

    def pop(self):
        if len(self.sent):
            return self.sent.pop(0)
        return None


class SmsCaptureSender(SmsSenderBaseClass):
    # A hack SMS service that records SMS messages
    SmsSenderBaseClass.messages = []

    def __init__(self):
        super().__init__()
        SmsSenderBaseClass.messages = []

    def send_sms(self, from_number, to_number, msg):
        SmsSenderBaseClass.messages.append(msg)
        return

    @classmethod
    def pop(cls):
        if len(SmsSenderBaseClass.messages):
            return SmsSenderBaseClass.messages.pop(0)
        return None





# declaring flask application
app = Flask(__name__)

csrf = CSRFProtect(app)


# calling the dev configuration
config = Config().dev_config

# making our application to use dev env
app.env = config.ENV

# load the secret key defined in the .env file
app.secret_key = os.environ.get("SECRET_KEY")

# PASSWORD_SALT secrets.SystemRandom().getrandbits(128)
app.config["SECURITY_PASSWORD_SALT"] = "101724723735873106751331085745587406834"

app.config["SECURITY_AUTO_LOGIN_AFTER_CONFIRM"] = True

# Allow signing in with a phone number or email
app.config["SECURITY_USER_IDENTITY_ATTRIBUTES"] = [
    {"email": {"mapper": uia_email_mapper, "case_insensitive": True}},
    {"us_phone_number": {"mapper": uia_phone_mapper}},
]
app.config["SECURITY_US_ENABLED_METHODS"] = ["password", "email", "sms"]

app.config["SECURITY_TOTP_SECRETS"] = {
    "1": "TjQ9Qa31VOrfEzuPy4VHQWPCTmRzCnFzMKLxXYiZu9B"
}
app.config['SECURITY_TOTP_ISSUER'] = os.environ.get("APP_NAME")


# These need to be defined to handle redirects
# As defined in the API documentation - they will receive the relevant context
app.config["SECURITY_LOGIN_ERROR_VIEW"] = "/redir/login-error"
app.config["SECURITY_POST_CONFIRM_VIEW"] = "/redir/confirmed"
app.config["SECURITY_CONFIRM_ERROR_VIEW"] = "/redir/confirm-error"
app.config["SECURITY_RESET_VIEW"] = "/redir/reset-password"
app.config["SECURITY_RESET_ERROR_VIEW"] = "/redir/reset-password-error"
app.config["SECURITY_REDIRECT_BEHAVIOR"] = "spa"

# CSRF protection is critical for all session-based browser UIs
# In general, most applications don't need CSRF on unauthenticated endpoints
app.config["SECURITY_CSRF_IGNORE_UNAUTH_ENDPOINTS"] = True

# Send Cookie with csrf-token. This is the default for Axios and Angular.
app.config["SECURITY_CSRF_COOKIE_NAME"] = "XSRF-TOKEN"
app.config["WTF_CSRF_CHECK_DEFAULT"] = False
app.config["WTF_CSRF_TIME_LIMIT"] = None

# have session and remember cookie be samesite (flask/flask_login)
app.config["REMEMBER_COOKIE_SAMESITE"] = "strict"
app.config["SESSION_COOKIE_SAMESITE"] = "strict"

# As of Flask-SQLAlchemy 2.4.0 it is easy to pass in options directly to the
# underlying engine. This option makes sure that DB connections from the pool
# are still valid. Important for entire application since many DBaaS options
# automatically close idle connections.
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {"pool_pre_ping": True}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

# Initialize a fake SMS service that captures SMS messages
app.config["SECURITY_SMS_SERVICE"] = "capture"
SmsSenderFactory.senders["capture"] = SmsCaptureSender

# Turn on all features (except passwordless since that removes normal login)
for opt in [
    "changeable",
    "recoverable",
    "registerable",
    "trackable",
    "confirmable",
    "two_factor",
    "unified_signin",
]:
    app.config["SECURITY_" + opt.upper()] = True

if os.environ.get("SETTINGS"):
    # Load settings from a file pointed to by SETTINGS
    app.config.from_envvar("SETTINGS")
    
# Path for our local sql lite database
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("SQLALCHEMY_DATABASE_URI_DEV")

# To specify to track modifications of objects and emit signals
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = os.environ.get("SQLALCHEMY_TRACK_MODIFICATIONS")

# Initialize standard Flask extensions
CaptureMail(app)
Babel(app)
# Enable CSRF on all api endpoints.
CSRFProtect(app)
db.init_app(app)
# Setup Flask-Security
app.security = Security(app, user_datastore)

bcrypt = Bcrypt(app)


# sql alchemy instance
# db = SQLAlchemy(app)


# Flask Migrate instance to handle migrations
migrate = Migrate(app, db)

# import api blueprint to register it with app
# from src.routes import api, mainNav
# app.register_blueprint(api, url_prefix="/api")
# app.register_blueprint(mainNav, url_prefix="/")

# import models to let the migrate tool know
from src.models.models import Post, Assignment, Categorization, Comment, Profile, Role, Tag, User

# Flask_Admin Setup
admin = Admin(app, name='Blog Site Admin')
admin.add_view(ModelView(Post, db.session))
admin.add_view(ModelView(Tag, db.session))
admin.add_view(ModelView(Categorization, db.session))
admin.add_view(ModelView(Comment, db.session))
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Profile, db.session))
admin.add_view(ModelView(Assignment, db.session))
admin.add_view(ModelView(Role, db.session))


# Flask_Bootstrap Setup
# serve locally for faster and offline development
app.config['BOOTSTRAP_SERVE_LOCAL'] = True

# set default button sytle and size, will be overwritten by macro parameters
app.config['BOOTSTRAP_BTN_STYLE'] = 'primary'
app.config['BOOTSTRAP_BTN_SIZE'] = 'sm'

# set default icon title of table actions
app.config['BOOTSTRAP_TABLE_VIEW_TITLE'] = 'Read'
app.config['BOOTSTRAP_TABLE_EDIT_TITLE'] = 'Update'
app.config['BOOTSTRAP_TABLE_DELETE_TITLE'] = 'Remove'
app.config['BOOTSTRAP_TABLE_NEW_TITLE'] = 'Create'
app.config['BOOTSTRAP_BOOTSWATCH_THEME'] = 'morph'

bootstrap = Bootstrap5(app)







# from flask import Flask
# import routes
# from src import db, Post, Tag, Categorization, Comment, User, Profile, Assignment, Role, main

# from dotenv import dotenv_values
# import os
# from flask_bootstrap import Bootstrap5
# from flask_wtf import CSRFProtect
# from flask_admin import Admin
# from flask_admin.contrib.sqla import ModelView
# from flask_migrate import Migrate

# config = {
#     **dotenv_values(".env"),  # load general variables
#     **dotenv_values(".env.shared"),  # load shared development variables
#     **dotenv_values(".env.secret"),  # load sensitive variables
#     **os.environ,  # override loaded values with environment variables
# }

# app = Flask(__name__)
# csrf = CSRFProtect(app)
# migrate = Migrate(app, db)

# admin = Admin(app, name='Blog Site Admin')
# admin.add_view(ModelView(Post, db.session))
# admin.add_view(ModelView(Tag, db.session))
# admin.add_view(ModelView(Categorization, db.session))
# admin.add_view(ModelView(Comment, db.session))
# admin.add_view(ModelView(User, db.session))
# admin.add_view(ModelView(Profile, db.session))
# admin.add_view(ModelView(Assignment, db.session))
# admin.add_view(ModelView(Role, db.session))

# app.config.from_object(Config)

# # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.getenv('DB_NAME', 'blog') + '.db'
# # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# # serve locally for faster and offline development
# app.config['BOOTSTRAP_SERVE_LOCAL'] = True

# # set default button sytle and size, will be overwritten by macro parameters
# app.config['BOOTSTRAP_BTN_STYLE'] = 'primary'
# app.config['BOOTSTRAP_BTN_SIZE'] = 'sm'

# # set default icon title of table actions
# app.config['BOOTSTRAP_TABLE_VIEW_TITLE'] = 'Read'
# app.config['BOOTSTRAP_TABLE_EDIT_TITLE'] = 'Update'
# app.config['BOOTSTRAP_TABLE_DELETE_TITLE'] = 'Remove'
# app.config['BOOTSTRAP_TABLE_NEW_TITLE'] = 'Create'
# app.config['BOOTSTRAP_BOOTSWATCH_THEME'] = 'morph'

# bootstrap = Bootstrap5(app)

# app.secret_key = os.getenv('SECRET_KEY', 'default_secret_key')

# # Initializes the app
# db.init_app(app)

# with app.app_context():
#     db.create_all()
#     print("Database created at:", app.config['SQLALCHEMY_DATABASE_URI'])

# app.register_blueprint(main)
# app.register_blueprint(routes, url_prefix='/api')

# if __name__ == '__main__':
#     app.run(debug=True)


