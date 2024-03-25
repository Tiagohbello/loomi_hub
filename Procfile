release: python manage.py migrate && python manage.py create_super_user
web: daphne loomi_hub.asgi:application --port $PORT --bind 0.0.0.0 -v2
