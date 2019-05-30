# Jellynote test backend

This is a python 3.7 test backend.
It supports http operations on User, Song, Notification.

Formatting is done with the Intellij default formatter (should be PEP8)

# Run

To run, ensure you have a running Postgres database.
Run the api with `python3 app.py [--conf CONF]`

# Setup

- Run `pip install -r requirements.txt`
- Create a database before running migrations

# Database

We use a postgres database.
By default, migrations are run on the `jellynote` database (cf `yoyo.ini` for tables and credentials)

To initialize it, run `yoyo apply -b`

# Tests

Unit tests are available in the `tests` package.
To run unit tests:
`python3 -m pytest`


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

- [x] dataclasses
- [x] serializers
- [x] persistence (users, songs)
- [ ] persistence (notification)
- [x] db migrations
- [x] configuration
- [x] routes (users, songs)
- [ ] routes notifications
- [x] tests (users, songs)
- [ ] tests notifications
- [x] prod run configuration with gunicorn
- [x] docker compose

Functional:
- [x] create, update, delete users
- [x] create, update, delete songs
- [x] docker image + docker compose 
- [ ] on song creation, generate notifications
- [ ] access notifications
- [ ] scenario data + script