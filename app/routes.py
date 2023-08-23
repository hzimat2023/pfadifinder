from flask import render_template
from app import app
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