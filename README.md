# Medicar API

Backend source code for the Intmed's Medicar challenge

The backend is a fully functioning REST API using:

 - Python
 - Django / Django-REST-Framework
 - Docker / Docker-Compose
 - Test Driven Development
 - Travis CI

## Getting started 🚀

To start project, run:

```
cd medicar_api
docker-compose up
```

The API will then be available at [http://127.0.0.1:8000](http://127.0.0.1:8000).

### Administration

Access http://localhost:8000/admin/. An admin account is automatically created for you when then
project starts. The credentials will be:

```
user: admin
password: 999999
```

## Testing

To run automated testing do

```bash
docker-compose run app sh -c "python manage.py test -v 2"
```

#### Create a user testing account

```bash
curl --request POST \
  --url http://localhost:8000/register/ \
  --header 'Content-Type: application/json' \
  --data '{
    "username": "user",
    "password": "pass"
}'
```

#### Get auth token

```bash
curl --request POST \
  --url http://localhost:8000/api-token-auth/ \
  --header 'Content-Type: application/json' \
  --data '{
    "username": "user",
    "password": "pass"
}'
```

#### Use the token to make requests

```bash
curl --request GET \
  --url http://localhost:8000/especialidades \
  --header 'Authorization: Token 446ec085093a7d4e30456e5ba8f66dbf3825f6c6'
```

🎇🎇🎇🎇
