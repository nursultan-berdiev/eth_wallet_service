#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "WAITING FOR POSTGRES..."

    while ! nc -z "$DB_HOST" "$DB_PORT"; do
      sleep 0.1
    done

    echo "POSTGRES STARTED"
fi

python manage.py migrate

exec "$@"