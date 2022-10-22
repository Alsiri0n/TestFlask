"""
Test application for testing CI/CD
"""
import os
from datetime import datetime
import psycopg2
import psycopg2.extras
from flask import Flask, g, render_template, request, url_for, make_response,redirect, flash, abort
from flask_sqlalchemy import SQLAlchemy
from flform.flform import flform
from fllogin.fllogin import fllogin
from flprofile.flprofile import flprofile
from flsql.flsql import Flsql


FLASK_HOST = str(os.environ.get('flask_host'))
FLASK_PORT = int(os.environ.get('flask_port'))
SECRET_KEY = str(os.environ.get('secret_key'))
POSTGRES_URL = str(os.environ.get('postgres_url'))
POSTGRES_PORT = str(os.environ.get('postgres_port'))
POSTGRES_USER = str(os.environ.get('postgres_user'))
POSTGRES_PW = str(os.environ.get('postgres_pw'))
POSTGRES_DB = str(os.environ.get('postgres_db'))

DB_URL = f'postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PW}\
        @{POSTGRES_URL}:{POSTGRES_PORT}/{POSTGRES_DB}'

app = Flask(__name__)
app.register_blueprint(flform, url_prefix='/form')
app.register_blueprint(fllogin, url_prefix='/login')
app.register_blueprint(flprofile, url_prefix='/profile')
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # silence the deprecation warning

app.config['TESTING'] = True

db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    psw = db.Column(db.String(500), nullable=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<users {self.id}>'

class Profiles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=True)
    old = db.Column(db.Integer)
    city = db.Column(db.String(100))

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return f'<profiles {self.id}>'


def connect_db():
    """
    This function create connection to dsatabase
    """
    conn = psycopg2.connect(host=POSTGRES_URL, database=POSTGRES_DB,
            user=POSTGRES_USER, password=POSTGRES_PW)
    return conn


def create_db():
    """
    Additional function for creation database
    """
    cur_db = connect_db()
    with app.open_resource('sql_db.sql', mode='r') as file:
        cur_db.cursor().execute(file.read())
    cur_db.commit()
    cur_db.close()


def get_db():
    """
    Get database link from global variable
    """
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


@app.teardown_appcontext
def close_db(error):
    """
    Close connection to database, if connected
    """
    if hasattr(g, 'link_db'):
        g.link_db.close()


@app.route('/index')
@app.route('/')
def index():
    """
    Main page of the site
    """
    cur_db = get_db()
    dbase = Flsql(cur_db)
    return render_template('index.html', menu=dbase.get_menu(), posts=dbase.get_posts_announcement())


@app.route('/about')
def about():
    """
    About page of the site
    """
    cur_db = get_db()
    dbase = Flsql(cur_db)
    return render_template('about.html', title='About', menu=dbase.get_menu())


@app.route('/set')
@app.route('/set/<theme>')
def set_theme(theme="light"):
    """
    This handler save theme in user cookies.
    """
    # print(request.referrer)
    res = make_response(redirect(url_for(".index")))
    # res = make_response(redirect(url_for(request.referrer.endpoint)))
    res.set_cookie("theme", theme)
    return res


@app.route('/add_post', methods=["GET", "POST"])
def add_post():
    """
    Adding post function
    """
    cur_db = get_db()
    dbase = Flsql(cur_db)

    if request.method == "POST":
        if len(request.form['name'])>4 and len(request.form['post'])>10:
            res = dbase.add_post(request.form['name'], request.form['post'])
            if not res:
                flash('Ошибка добавления статьи', category='error')
            else:
                flash('Статья добавлена успешно', category='success')
        else:
            flash('Ошибка добавления статьи', category='error')
    return render_template('add_post.html', menu=dbase.get_menu(), title='Добавление статьи')


@app.route('/post/<int:id_post>')
def show_post(id_post):
    """
    Function showing post by id
    """
    cur_db = get_db()
    dbase = Flsql(cur_db)
    title, post = dbase.get_post(id_post).values()
    if not title:
        abort(404)

    return render_template('post.html', menu=dbase.get_menu(), title=title, post=post)


@app.errorhandler(404)
def page_not_found(error):
    """
    404 Error Page
    """
    cur_db = get_db()
    dbase = Flsql(cur_db)
    return render_template('page404.html', menu=dbase.get_menu(), title="Страница не найдена"), 404

if __name__ == "__main__":
    app.run(host=FLASK_HOST, port=FLASK_PORT)
