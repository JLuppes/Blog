from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
import flask_login
# from src import db
from flask_security.models import fsqla_v2 as fsqla
from flask_security import SQLAlchemyUserDatastore
from flask_sqlalchemy import SQLAlchemy
from src.services.database import db


# Create database connection object
# db = SQLAlchemy()

# Define models
fsqla.FsModels.set_db_info(db)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    content = db.Column(db.String(10000))
    created = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    deleted = db.Column(db.Boolean, default=False)
    # Relationships
    categories = db.relationship('Categorization', backref='post', lazy=True)
    comments = db.relationship('Comment', backref='post', lazy=True)


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    # Relationships
    categorizations = db.relationship(
        'Categorization', backref='tag', lazy=True)


class Categorization(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'))


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    content = db.Column(db.String(1000))
    deleted = db.Column(db.Boolean, default=False)
    created = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated = db.Column(db.DateTime, default=datetime.now(timezone.utc))


class User(db.Model, fsqla.FsUserMixin):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100))
    display_name = db.Column(db.String(100))
    deleted = db.Column(db.Boolean, default=False)
    # Relationships
    posts = db.relationship('Post', backref='user', lazy=True)
    comments = db.relationship('Comment', backref='user', lazy=True)
    assignments = db.relationship('Assignment', backref='user', lazy=True)
    profile = db.relationship(
        'Profile', backref='user', lazy=True, uselist=False)
    us_phone_number = db.Column(db.String(128), unique=True, nullable=True)


class Profile(db.Model):
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    name = db.Column(db.String(100))
    bio = db.Column(db.String(1000))
    location = db.Column(db.String(100))
    avatar = db.Column(db.String(100))
    deleted = db.Column(db.Boolean, default=False)
    created = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated = db.Column(db.DateTime, default=datetime.now(timezone.utc))


class Assignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    deleted = db.Column(db.Boolean, default=False)
    created = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))


class Role(db.Model, fsqla.FsRoleMixin):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1000))
    # Relationships
    assignments = db.relationship('Assignment', backref='role', lazy=True)


# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
