import os
from dotenv import load_dotenv
from flask import Flask
from flask import jsonify
from sentry_sdk.integrations.flask import FlaskIntegration
import sentry_sdk
from .summarizer import youtube_video


def create_app(testing: bool = True):
    load_dotenv()

    sentry_sdk.init(
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
        video_url = 'https://www.youtube.com/watch?v=-3toF-B2lEk'

        data = {
            'summary': youtube_video.summarize(video_url)
        }

        return jsonify(data)

    return app
