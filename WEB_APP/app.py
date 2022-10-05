import os
from flask import Flask

FLASK_HOST = str(os.environ.get('flask_host'))
FLASK_PORT = int(os.environ.get('flask_port'))

app = Flask(__name__)


@app.route('/')
def index():
    return 'ok\n'


if __name__ == "__main__":
    app.run(host= FLASK_HOST, port= FLASK_PORT)
