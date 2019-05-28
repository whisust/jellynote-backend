# Jellynote test backend

This is a python 3.7 test backend.
It supports http operations on User, Song, Notification.

# Run

To run, ensure you have a running Postgres database.

# Setup

- Install PostgreSQL
- Run `pip install -r requirements.txt`

# Database

We use a postgres database.
By default, migrations are run on the `jellynote` database (cf `yoyo.ini`)

To initialize it, run `yoyo apply -b`


# Tests

TODO

# Docker

TODO

# Metrics

TODO