from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm
@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Ammann'}
    posts = [
        {   
            'author': {'username': 'Andi'},
            'body': 'Schöner Abend hier in Zürich!'
        },
        {
            'author': {'username': 'Susanne'},
            'body': 'Der Unterricht war heute mal gut!'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)


@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title='Sign In', form=form)