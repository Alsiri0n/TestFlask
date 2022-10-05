"""
Test application for testing CI/CD
"""
import os
from flask import Flask

FLASK_HOST = str(os.environ.get('flask_host'))
FLASK_PORT = int(os.environ.get('flask_port'))

app = Flask(__name__)


@app.route('/index')
@app.route('/')
def index():
    """
    Main page of the site
    """
    return 'ok\n'

@app.route('/about')
def about():
    """
    About page of the site
    """
    return "<h1>О сайте</h1>"


if __name__ == "__main__":
    app.run(host=FLASK_HOST, port=FLASK_PORT)
