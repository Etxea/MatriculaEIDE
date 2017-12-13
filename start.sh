#!/bin/bash
python manage.py migrate                  # Apply database migrations
python manage.py collectstatic --noinput  # Collect static files

# Prepare log files and start outputting logs to stdout
touch /var/log/gunicorn.log
touch /var/log/access.log
tail -n 0 -f /var/log/access.log /var/log/gunicorn.log &

# Start Gunicorn processes
echo Starting Gunicorn.
exec gunicorn matriculas.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 --error-logfile /var/log/gunicorn.log --log-file /var/log/access.log
