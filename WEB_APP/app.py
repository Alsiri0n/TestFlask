"""
Test application for testing CI/CD
"""
import os
from flask import Flask, render_template, url_for, make_response,redirect
from flform.flform import flform


FLASK_HOST = str(os.environ.get('flask_host'))
FLASK_PORT = int(os.environ.get('flask_port'))

app = Flask(__name__)
app.register_blueprint(flform, url_prefix='/flokoform')

myMenu = [{"name": "Установка", "url": "install-flask"},
          {"name": "Первое приложение", "url": "first-app"},
          {"name": "Обратная связь", "url": "flokoform"}]
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
    res = make_response(redirect(url_for(".index")))
    res.set_cookie("theme", theme)
    return res

if __name__ == "__main__":
    app.run(host=FLASK_HOST, port=FLASK_PORT)
