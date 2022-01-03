flask db upgrade
gunicorn -w 4 run:app --bind 0.0.0.0:5000