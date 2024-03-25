release: python manage.py migrate
web: daphne loomi_hub.asgi:application --port $PORT --bind 0.0.0.0 -v2