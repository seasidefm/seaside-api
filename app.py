import json
from flask import Flask, request
from dotenv import load_dotenv

from services.locator import Locator

app = Flask(__name__)

# Setup area
# ==========================

load_dotenv()
service_locator = Locator()

# ==========================


@app.route("/")
def hello_world():
    return {
        "hello": "world"
    }


@app.get("/video")
def get_video():
    return service_locator.videos.get_movie_details()


@app.route("/health")
def health():
    return "OK"


@app.post("/songs/new")
def new_song():
    data = request.json
    if data['song']:
        return service_locator.songs.add_current_song(data['song'])
    else:
        return "`song` key is required!", 400


@app.get("/songs/current")
def current_song():
    return service_locator.songs.current_song()


@app.get("/songs/last")
def last_song():
    return service_locator.songs.last_song()


@app.post("/faves/new")
def new_fave():
    service_locator.faves.save_song()
    return "OK"


if __name__ == "__main__":
    print("Starting SeasideFM Beta API...")
    app.run(host="0.0.0.0", port=4000, debug=True)
