"""
Test application for testing CI/CD
"""
import os
import psycopg2
import psycopg2.extras
from datetime import datetime
from flask import Flask, g, render_template, url_for, make_response,redirect
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
    '''
    This funcction create connection to dsatabase
    '''
    conn = psycopg2.connect(host=POSTGRES_URL, database=POSTGRES_DB, user=POSTGRES_USER, password=POSTGRES_PW)
    return conn


def create_db():
    '''
    Additional function for creation database
    '''
    cur_db = connect_db()
    with app.open_resource('sql_db.sql', mode='r') as f:
        cur_db.cursor().execute(f.read())
    cur_db.commit()
    cur_db.close()


def get_db():
    '''
    Get database link from global variable
    '''
    if not hasattr(g, 'link_db'):
        print(f'URL - {POSTGRES_URL}')
        print(f'DB - {POSTGRES_DB}')
        print(f'USER - {POSTGRES_USER}')
        print(f'PW - {POSTGRES_PW}')
        g.link_db = connect_db()
    return g.link_db


@app.teardown_appcontext
def close_db(error):
    '''
    Close connection to database, if connected
    '''
    if hasattr(g, 'link_db'):
        g.link_db.close()


myMenu = [{"name": "Установка", "url": "install-flask"},
          {"name": "Первое приложение", "url": "first-app"},
          {"name": "Обратная связь", "url": "form"}]

@app.route('/index')
@app.route('/')
def index():
    """
    Main page of the site
    """
    db = get_db()
    dbase = Flsql(db)
    return render_template('index.html', menu=dbase.get_menu())

@app.route('/about')
def about():
    """
    About page of the site
    """
    return render_template('about.html', title='About', menu=myMenu)

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

@app.errorhandler(404)
def page_not_found(error):
    """
    404 Error Page
    """
    return render_template('page404.html', title="Страница не найдена"), 404

if __name__ == "__main__":
    app.run(host=FLASK_HOST, port=FLASK_PORT)
