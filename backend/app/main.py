import os
from dotenv import load_dotenv
from flask import Flask
from sentry_sdk.integrations.flask import FlaskIntegration
import sentry_sdk


def create_app(testing: bool = True):
    load_dotenv()

    sentry_sdk.init(git
        dsn=os.environ.get("SENTRY_DSN"),
        enable_tracing=True,
        integrations=[FlaskIntegration()],
    )

    app = Flask(__name__)

    app.config['DEBUG'] = os.environ.get('FLASK_DEBUG')

    @app.route("/")
    def index():
        return f"<p>Hello, World!</p>"

    @app.route("/api/summarize")
    def summarize():
        division_by_zero = 1 / 0
        return f"<p>Summarize</p>"

    return app
