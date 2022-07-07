import os
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

from routes import blueprint
from services.locator import Locator
from shared.structures import AppResult

app = Flask(__name__)

# Setup area
# ==========================

# Enable CORS for ALL hosts
CORS(app)

load_dotenv(verbose=True)
sentry_dsn = os.environ.get('SENTRY_DSN')
if sentry_dsn:
    sentry_sdk.init(
        dsn=sentry_dsn,
        integrations=[FlaskIntegration()],
        environment="production",
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production.
        traces_sample_rate=1.0
    )
else:
    print("No SENTRY_DSN found in env, skipping setup")

service_locator = Locator()

# ==========================


# Assign Routes
# ==========================
@app.route("/")
def hello_world():
    return {
        "hello": "world"
    }


@app.get("/video")
def get_video():
    return AppResult(
        message="Movie details for stream",
        data=service_locator.videos.get_movie_details()
    ).response_tuple()


@app.route("/health")
def health():
    return AppResult(
        message="Health status measurements for app services",
        data=["OK"]
    ).response_tuple()


app.register_blueprint(blueprint)

# ==========================

port = os.environ.get('PORT') or 4000
if __name__ == "__main__":
    print("Starting SeasideFM Beta API...")
    if os.environ.get('IS_PRODUCTION') is not None:
        from waitress import serve
        import logging
        logger = logging.getLogger('waitress')
        logger.setLevel(logging.INFO)

        serve(app=app, port=port)
    else:
        app.run(host="0.0.0.0", port=port, debug=True)
