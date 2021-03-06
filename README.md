# seaside-api
The python-based unified API for the SeasideFM ecosystem

## Installation
This is a typical Python application, so use your favorite virtual environment wrapper:
```shell
python3 -m venv venv
```

And get your deps:
```shell
source venv/bin/activate
pip install -r requirements.txt
```

## Running the app
First copy `.example.env` to `.env` and populate values as required.

```shell
cp .example.env .env
```

Then, when env values are populated, the following command will run the project locally:

```shell
# -u is optional, but guarantees the output is sent to stdout instead of being eaten
python -u app.py
```

## Deploying
This application is deployed using docker via a kubernetes stack running on a 
Raspberry Pi cluster.

Make sure you're logged in to the correct docker registry, then run:

```shell
make deploy
```

This will build the docker image for arm64, push to the registry, then rollout the
kubernetes deployment with the new image.
