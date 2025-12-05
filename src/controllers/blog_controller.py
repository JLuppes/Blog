from flask import Blueprint, render_template, request, redirect, url_for
from src.models.models import Post, Assignment, Categorization, Comment, Profile, Role, Tag, User

blog = Blueprint('blog', __name__)


@blog.route('/')
def blog_home():
    post_list = Post.query.all()

    return render_template('blog.html.jinja', posts=post_list)


@blog.route('/post/<int:id>')
def single_post(id):
    requested_post = Post.query.get_or_404(id)

    return render_template('posts/singlepost.html.jinja', post=requested_post)


@blog.route('/post/new', methods=['GET', 'POST'])
def new_post():
    if request.method == 'POST':
        newpost = Post()
        user = request.form.get('userID')
        content = request.form.get('content')

    return render_template('posts/newpost.html.jinja')
