python manage.py wait_for_db &&
python manage.py makemigrations &&
python manage.py migrate &&
python manage.py setup_test_data &&
python manage.py createsuperuser --noinput 2&>/dev/null
