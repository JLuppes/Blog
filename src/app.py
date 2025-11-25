from flask import Flask
from config import Config
from models import db, Post, Tag, Categorization, Comment, User, Profile, Assignment, Role
from controllers import main
from blog import blog
from dotenv import dotenv_values
import os
from flask_bootstrap import Bootstrap5
from flask_wtf import CSRFProtect
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_migrate import Migrate

config = {
    **dotenv_values(".env"),  # load general variables
    **dotenv_values(".env.shared"),  # load shared development variables
    **dotenv_values(".env.secret"),  # load sensitive variables
    **os.environ,  # override loaded values with environment variables
}

app = Flask(__name__)
csrf = CSRFProtect(app)
migrate = Migrate(app, db)

admin = Admin(app, name='Blog Site Admin')
admin.add_view(ModelView(Post, db.session))
admin.add_view(ModelView(Tag, db.session))
admin.add_view(ModelView(Categorization, db.session))
admin.add_view(ModelView(Comment, db.session))
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Profile, db.session))
admin.add_view(ModelView(Assignment, db.session))
admin.add_view(ModelView(Role, db.session))

app.config.from_object(Config)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.getenv('DB_NAME', 'blog') + '.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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

app.secret_key = os.getenv('SECRET_KEY', 'default_secret_key')

# Initializes the app
db.init_app(app)

with app.app_context():
    db.create_all()
    print("Database created at:", app.config['SQLALCHEMY_DATABASE_URI'])

app.register_blueprint(main)

if __name__ == '__main__':
    app.run(debug=True)
