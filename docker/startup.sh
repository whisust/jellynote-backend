#!/bin/bash -ex

echo "Waiting for PG to be up"
sleep 10
echo "Waited enough"
if [[ "$RUN_MIGRATION" == "true" ]] ; then
    echo "Running migrations on postgresql://$DB_USER:$DB_PASSWORD@$DB_HOST:$DB_PORT/$DB_NAME"
    yoyo apply --batch --no-config-file --database "postgresql://$DB_USER:$DB_PASSWORD@$DB_HOST:$DB_PORT/$DB_NAME" ./resources/migrations
fi
echo "Starting api..."
cd api
PYTHONUNBUFFERED=TRUE gunicorn --bind 0.0.0.0:$SERVER_PORT \
                               --error-logfile - \
                               --access-logfile - \
                               --capture-output \
                               --log-level info \
                               app:app
