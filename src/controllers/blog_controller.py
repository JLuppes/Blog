from flask import Blueprint, render_template, request, redirect, url_for
from src.models.models import Post, Assignment, Categorization, Comment, Profile, Role, Tag, User
from flask_wtf import FlaskForm
from wtforms import StringField, validators, widgets, TextAreaField, HiddenField
from flask_login import login_required
from src.services.database import db

blog = Blueprint('blog', __name__)


class CommentForm(FlaskForm):
    comment_content = TextAreaField('Comment Content', render_kw={
        "rows": 3, "cols": 30})
    user_id = HiddenField()
    post_id = HiddenField()


@blog.route('/')
def blog_home():
    commentform = CommentForm()
    post_list = Post.query.all()

    return render_template('blog.html.jinja', posts=post_list, commentform=commentform)


@blog.route('/post/<int:id>')
def single_post(id):
    commentform = CommentForm()
    requested_post = Post.query.get_or_404(id)

    return render_template('posts/singlepost.html.jinja', post=requested_post, commentform=commentform)


class BlogPostForm(FlaskForm):
    post_content = TextAreaField('Post Content', render_kw={
                                 "rows": 10, "cols": 80})
    user_id = HiddenField()


@blog.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    # if request.method == 'POST':
    #     newpost = Post()
    #     user = request.form.get('userID')
    #     content = request.form.get('content')

    form = BlogPostForm()
    commentform = CommentForm()
    if request.method == 'POST':

        try:

            new_post = Post(
                user_id=request.form.get("user_id"),
                content=request.form.get("post_content")
            )

            db.session.add(new_post)
            db.session.commit()

        except Exception as e:
            error = "Error adding new post."
            return render_template('posts/newpost.html.jinja', form=form, error=error)

        return redirect(url_for('mainNav.blog.blog_home'))

    return render_template('posts/newpost.html.jinja', form=form, commentform=commentform)


@blog.route('/post/comment/new', methods=['POST'])
@login_required
def new_comment():

    try:
        new_comment = Comment(user_id=request.form.get("user_id"),
                              content=request.form.get("comment_content"),
                              post_id=request.form.get("post_id"))
        db.session.add(new_comment)
        db.session.commit()
    except Exception as e:
        error = "Adding comment failed!" + str(e)
        return render_template("blog.html.jinja", error=error)
    return redirect(url_for('mainNav.blog.single_post', id=request.form.get("post_id")))
