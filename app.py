import os
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from flask import Flask, request
from dotenv import load_dotenv

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
@update_heat
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


@app.get("/superfaves")
def superfaves_for_user():
    user = request.args.get('user_id')
    return AppResult(
        message="User's superfave songs",
        data=service_locator.superfaves.get_songs(user)
    ).response_tuple()


@app.delete("/faves")
@token_required
@update_heat
def delete_fave():
    data = request.json
    fave_id = data.get('fave_id')

    response = None
    if fave_id:
        result = service_locator.faves.delete_fave(fave_id)
        if result:
            response = AppResult(message="Favorite successfully deleted", data={
                "data": True
            })
        else:
            response = AppError(
                message="Something went wrong deleting favorite!",
                error="Could not delete favorite, please check ID"
            )
    else:
        response = AppError(
            message="Fave ID is missing from request body",
            error="`fave_id` is missing or improper format",
            code=400
        )

    return response.response_tuple()


@app.delete("/superfaves")
@token_required
@update_heat
def delete_superfave():
    data = request.json
    fave_id = data.get('fave_id')

    response = None
    if fave_id:
        result = service_locator.superfaves.delete_fave(fave_id)
        if result:
            response = AppResult(message="Superfave successfully deleted", data={
                "data": True
            })
        else:
            response = AppError(
                message="Something went wrong deleting superface!",
                error="Could not delete superfave, please check ID"
            )
    else:
        response = AppError(
            message="Fave ID is missing from request body",
            error="`fave_id` is missing or improper format",
            code=400
        )

    return response.response_tuple()



@app.post("/faves")
@token_required
@update_heat
def new_fave():
    data = request.json

    user_id = data.get('user_id')
    song = data.get('song')
    if user_id:
        result =\
            service_locator.faves.save_last(user_id)\
            if song == "last" else\
            service_locator.faves.save_song(user_id)

        formatted = AppResult(
            message="Added current song as favorite",
        ) if result else AppError(
            message="Already user favorite",
            error=f"Already a favorite for {user_id}",
            code=409
        )

        return formatted.response_tuple()
    else:
        return AppError(
            message="User ID key is missing or wrong format",
            error="`user_id` key is required to favorite current song",
            code=400
        ).response_tuple()


@app.post("/faves/superfave")
@token_required
@update_heat
def new_superfave():
    data = request.json

    user_id = data.get('user_id')
    song = data.get('song')
    if user_id:
        result =\
            service_locator.superfaves.save_last(user_id) \
            if song == "last" else \
            service_locator.superfaves.save_song(user_id)

        formatted = AppResult(
            message="Added current song as superfave",
        ) if result else AppError(
            message="Already user superfave",
            error=f"Already a superfave for {user_id}",
            code=409
        )

        return formatted.response_tuple()
    else:
        return AppError(
            message="User ID key is missing or wrong format",
            error="`user_id` key is required to super-fave current song",
            code=400
        ).response_tuple()


@app.get('/heat')
def get_heat():
    return AppResult(
        message="Current heat level",
        data=service_locator.heat.get_current_heat()
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
