import os
from dotenv import load_dotenv
from flask import Flask
from flask import request
from flask import jsonify
from sentry_sdk.integrations.flask import FlaskIntegration
import sentry_sdk
from .summarizer import youtube_video
import re


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
        return f"<p>Index</p>"

    @app.route("/api/summarize", methods=['POST'])
    def summarize():
        if not request.json:
            return jsonify({'error': 'Request must be JSON'}), 400

        if 'youtube_video_url' not in request.json:
            return jsonify({'error': 'Missing YouTube URL'}), 400

        youtube_video_url = request.json.get('youtube_video_url')

        if not re.match(r'(https?://)?(www\.)?youtube\.com/watch\?v=[a-zA-Z0-9_-]{11}', youtube_video_url):
            return jsonify({'error': 'Invalid YouTube URL'}), 400

        data = {
            'summary': youtube_video.summarize(youtube_video_url)
        }

        return jsonify(data)

    return app
