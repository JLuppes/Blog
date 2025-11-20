from flask import Blueprint, render_template, request, redirect, url_for
from models import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html.jinja')
