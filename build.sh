
heroku login
heroku create
git push heroku master

heroku run python manage.py migrate
heroku open

git push heroku master

heroku config:set NGINX_WORKERS=4
heroku config:set API_URL=http://api.example.com/
heroku config:set API_PREFIX_PATH=/api/
heroku config:set FORCE_HTTPS=true
