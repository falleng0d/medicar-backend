# Medicar API

Backend source code for the Intmed's Medicar challenge

The backend is a fully functioning REST API using:

 - Python
 - Django / Django-REST-Framework
 - Docker / Docker-Compose
 - Test Driven Development using:
     - Auto generated mock data with FactoryBoy
     - Travis CI
 - Heroku-ready

## Getting started 🚀

### Remote
The api is already deployed to Heroku and is available at [https://medicar-api.herokuapp.com](https://medicar-api.herokuapp.com).

The deployment setup is included on the repository

### Local
To start project, run:

```
cd backend
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

## Projec Architeture

![Architeture](./architeture.png)

## Project Structure

Simplified

```
.
├── Dockerfile
├── LICENSE
├── README.md
├── app
│  ├── app
│  ├── appointment
│  ├── core
│  ├── manage.py
│  ├── medic
│  ├── schedule
│  ├── specialty
│  └── user
├── architeture.png
├── docker-compose.yml
├── model.drawio
└── requirements.txt
```

Expanded

```
.
├── Dockerfile
├── LICENSE
├── README.md
├── app
│   ├── app
│   │   ├── asgi.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── appointment
│   │   ├── apps.py
│   │   ├── serializers.py
│   │   ├── tests
│   │   │   └── test_api.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── core
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── management
│   │   │   └── commands
│   │   │       ├── setup_test_data.py
│   │   │       └── wait_for_db.py
│   │   ├── migrations
│   │   │   └── 0001_initial.py
│   │   ├── models.py
│   │   ├── tests
│   │   │   ├── factories.py
│   │   │   ├── helpers.py
│   │   │   ├── test_auth.py
│   │   │   └── test_commands.py
│   │   └── utilities.py
│   ├── manage.py
│   ├── medic
│   │   ├── apps.py
│   │   ├── serializers.py
│   │   ├── tests
│   │   │   └── test_api.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── schedule
│   │   ├── apps.py
│   │   ├── serializers.py
│   │   ├── tests
│   │   │   └── test_api.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── specialty
│   │   ├── apps.py
│   │   ├── serializers.py
│   │   ├── tests
│   │   │   └── test_api.py
│   │   ├── urls.py
│   │   └── views.py
│   └── user
│       ├── apps.py
│       ├── serializers.py
│       ├── tests
│       │   └── test_api.py
│       ├── urls.py
│       └── views.py
├── architeture.png
├── docker-compose.yml
├── model.drawio
└── requirements.txt

17 directories, 48 files

```

🎇🎇🎇🎇 
