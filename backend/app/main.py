import os
from dotenv import load_dotenv
from flask import Flask

load_dotenv()

def create_app(testing: bool = True):
    app = Flask(__name__)

    app.config['DEBUG'] = os.environ.get('FLASK_DEBUG')

    @app.route("/")
    def index():
        return f"<p>Hello, World!</p>"

    return app
