import os
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from flask import Flask, request
from dotenv import load_dotenv

from controllers.token import token_required
from services.locator import Locator
from shared.structures import AppError, AppResult

app = Flask(__name__)

# Setup area
# ==========================

load_dotenv()
sentry_sdk.init(
    dsn="https://f50589cc78d24d5a9e3c2e2466aa72b5@o1076291.ingest.sentry.io/6247312",
    integrations=[FlaskIntegration()],

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0
)
service_locator = Locator()

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


@app.post("/songs/new")
@token_required
def new_song():
    data = request.json
    try:
        if data['song']:
            result = service_locator.songs.add_current_song(data['song'])
            return AppResult(
                message=f"Added {data['song']} to history",
                data=result
            ).response_tuple()
        else:
            return AppError(
                message="Song key is missing or incorrect format",
                error="`song` key is required!",
                code=400
            ).response_tuple()
    except Exception as e:
        return AppError(
            message="Something went wrong",
            error=str(e),
            code=500
        ).response_tuple()


@app.get("/songs/current")
def current_song():
    return AppResult(
        message="Current song",
        data=service_locator.songs.current_song().to_dict()
    ).response_tuple()


@app.get("/songs/last")
def last_song():
    return AppResult(
        message="Last song",
        data=service_locator.songs.last_song().to_dict()
    ).response_tuple()


@app.get("/faves/user")
def faves_for_user():
    user = request.args.get('user_id')
    return AppResult(
        message="User's favorite songs",
        data=service_locator.faves.get_songs(user)
    ).response_tuple()


@app.post("/faves/current")
@token_required
def new_fave():
    data = request.json
    if data.get('user') is not None:
        result = service_locator.faves.save_song(data.get('user'))

        formatted = AppResult(
            message="Added current song as favorite",
        ) if result else AppError(
            message="Already user favorite",
            error=f"Already a favorite for {data.get('user')}",
            code=409
        )

        return formatted.response_tuple()
    else:
        return AppError(
            message="User key is missing or wrong format",
            error="`user` key is required to favorite current song",
            code=400
        ).response_tuple()


if __name__ == "__main__":
    print("Starting SeasideFM Beta API...")
    if os.environ.get('IS_PRODUCTION') is not None:
        from waitress import serve
        serve(app=app, port=4000)
    else:
        app.run(host="0.0.0.0", port=4000, debug=True)
