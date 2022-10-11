"""
Test application for testing CI/CD
"""
import os
from flask import Flask, render_template, url_for, make_response,redirect
from flform.flform import flform
from fllogin.fllogin import fllogin


FLASK_HOST = str(os.environ.get('flask_host'))
FLASK_PORT = int(os.environ.get('flask_port'))
SECRET_KEY = str(os.environ.get('secret_key'))


app = Flask(__name__)
app.register_blueprint(flform, url_prefix='/form')
app.register_blueprint(fllogin, url_prefix='/login')
app.config['SECRET_KEY'] = SECRET_KEY

myMenu = [{"name": "Установка", "url": "install-flask"},
          {"name": "Первое приложение", "url": "first-app"},
          {"name": "Обратная связь", "url": "form"}]

@app.route('/index')
@app.route('/')
def index():
    """
    Main page of the site
    """
    return render_template('index.html', menu=myMenu)

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
