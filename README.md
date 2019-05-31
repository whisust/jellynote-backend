# Jellynote test backend

This is a python 3.7 prod-ready (almost) app backend.
It supports http operations on User, Song, Notification.

Formatting is done with the Intellij default formatter (should be PEP8)

# Run

To run, ensure you have a running Postgres database.
Run the api in dev mode with `python3 app.py`

# Setup

- Run `pip install -r requirements.txt`
- Create a database before running migrations

# Database

We use a postgres database.
By default, migrations are run on the `jellynote` database (cf `yoyo.ini` for tables and credentials)

To initialize it, run `yoyo apply -b`

# Tests

Unit/Intergation tests are available in the `tests` package.
To run them, you need an available DB and then:
`python3 -m pytest`

:warn: Tests work fine on my computer with the Intellij runner, but path is not resolved as it should be, thus the command fails...


# Docker

To build the container, run
`docker build . -t jellynote-api:latest`

To boot the system, run
`docker-compose up`

It starts Postgres + the latest version of the backend.
The api should be available on localhost:8000

# Metrics

TODO

# Known problems

`dataclass-json` does not support yet serde for enums, the commit to handle it have been done a few days ago (26 May) so there will be a few boilerplate lines waiting for the last version.


# Checklist

Technical:
- [x] project setup
- [x] dataclasses
- [x] serializers
- [x] persistence (users, songs)
- [x] persistence (notification)
- [x] db migrations
- [x] configuration
- [x] routes (users, songs)
- [x] routes notifications
- [x] tests (users, songs)
- [x] tests notifications
- [x] gen notifications
- [x] prod run configuration with gunicorn
- [x] docker compose

Functional:
- [x] create, update, delete users
- [x] create, update, delete songs
- [x] docker image + docker compose 
- [x] on song creation, generate notifications
- [x] access notifications
- [x] scenario data + script

# Test scenario

Start the 
Create a few users :
`for usr in $(ls examples/user*) ; do curl -X POST http://localhost:8000/users -H 'Content-Type: application/json' -d @$usr ; done`

Post a few songs :
`for song in $(ls examples/song*) ; do curl -X POST http://localhost:8000/songs -H 'Content-Type: application/json' -d @$song ; done`

Check for notifications :
`curl -X GET localhost:8000/notifications/<userid>`