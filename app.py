import os
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from flask import Flask, request
from dotenv import load_dotenv

from routes import blueprint
from controllers.token import token_required
from services.locator import Locator
from shared.structures import AppError, AppResult
from utils.heat_setter import update_heat

app = Flask(__name__)

# Setup area
# ==========================

load_dotenv()
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
app.register_blueprint(blueprint)
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


if __name__ == "__main__":
    print("Starting SeasideFM Beta API...")
    if os.environ.get('IS_PRODUCTION') is not None:
        from waitress import serve
        import logging
        logger = logging.getLogger('waitress')
        logger.setLevel(logging.INFO)

        serve(app=app, port=4000)
    else:
        app.run(host="0.0.0.0", port=4000, debug=True)
