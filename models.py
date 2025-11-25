from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
import flask_login
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from app import app

db = SQLAlchemy()
admin = Admin(app, name='Blog Site')


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('user.id'))
    content = db.Column(db.String(10000))
    created = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    deleted = db.Column(db.Boolean, default=False)
    # Relationships
    categories = db.relationship('Categorization', backref='post', lazy=True)
    posts = db.relationship('Comment', backref='post', lazy=True)
admin.add_view(ModelView(Post, db.session))


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    # Relationships
    categorizations = db.relationship(
        'Categorization', backref='tag', lazy=True)
admin.add_view(ModelView(Tag, db.session))


class Categorization(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'))
admin.add_view(ModelView(Categorization, db.session))


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    content = db.Column(db.String(1000))
    deleted = db.Column(db.Boolean, default=False)
    created = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated = db.Column(db.DateTime, default=datetime.now(timezone.utc))
admin.add_view(ModelView(Comment, db.session))


class User(db.Model, flask_login.UserMixin):
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
admin.add_view(ModelView(User, db.session))


class Profile(db.Model):
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    name = db.Column(db.String(100))
    bio = db.Column(db.String(1000))
    location = db.Column(db.String(100))
    avatar = db.Column(db.String(100))
    deleted = db.Column(db.Boolean, default=False)
    created = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated = db.Column(db.DateTime, default=datetime.now(timezone.utc))
admin.add_view(ModelView(Profile, db.session))


class Assignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    deleted = db.Column(db.Boolean, default=False)
    created = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
admin.add_view(ModelView(Assignment, db.session))


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1000))
    # Relationships
    assignments = db.relationship('Assignment', backref='role', lazy=True)
admin.add_view(ModelView(Role, db.session))
