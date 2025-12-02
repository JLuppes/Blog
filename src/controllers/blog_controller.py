from flask import Blueprint, render_template, request, redirect, url_for

blog = Blueprint('blog', __name__)

@blog.route('/')
def blog_home():
    return render_template('blog.html.jinja')
