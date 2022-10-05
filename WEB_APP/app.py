"""
Test application for testing CI/CD
"""
import os
from flask import Flask, render_template

FLASK_HOST = str(os.environ.get('flask_host'))
FLASK_PORT = int(os.environ.get('flask_port'))

app = Flask(__name__)

myMenu = ['Установка', 'Первое приложение', 'Обратная связь']
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


if __name__ == "__main__":
    app.run(host=FLASK_HOST, port=FLASK_PORT)
