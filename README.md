# base-python
Master repo for a python based component within a codeontap based product/project

## Layout

* ./src \- python source 
* ./devops/codeontap \- files to support deployment to codeontap environments
* ./devops/docker \- docker packaging for codeontap environments
* ./devops/docker-local \- docker packaging for local development
* ./docs \- repo specific documentation

Docker files are designed to be run from the root of the repo. Thus to test locally, copy the files in ./devops/docker-local to ./.

## Basics

The repo is designed so that it can be immediately forked to create a python based component that can be run locally or within a codeontap environment.

Contributors to the repo are expected to perform their feature submissions in the form of a pull request.

## Developer

### Getting started

1. Fork the repo.
1. Create a .env file in the ./src repo containing the enviroment variables for the required functionality (see below). Note that this file is excluded from the repo via .gitignore, and will be explicitly deleted 
if the code in run a codeontap environment.
1. Copy ./devops/docker-local to ./. This will permit the app to be run locally as follows;

```
TODO: Add example command of running app locally
```

1. Search for all occurrences of "app_dir" in file names and content and replace with the package name to be used for the component. 

The repo code will run as is without the replacement. If undertaking a probationary activity, skip the replacement step. 

### Code Style

Code is expected to follow the following guidelines;

* [code style](https://www.python.org/dev/peps/pep-0008/)
* [docstrings](https://www.python.org/dev/peps/pep-0257/)
* [comments](https://www.python.org/dev/peps/pep-0008/#comments)

## Devops for codeontap

### Getting started

1. Copy ./devops/codeontap/container_{containerid}.ftl to the solutions directory in the product codeontap config repos. 
1. Replace "{containerid}" with the id used for the component in the solution file.
1. Set up build job for the code repo based on the buildPython.sh script.

### Run modes

When run as a docker container, the codeontap docker packaging supports running the code in multiple "modes". The modes are

1. WEB \- long running process providing a website (default)
1. TASK \- run-to-completion task invoked via manage.py
1. WORKER \- celery worker
1. BEAT \- celery beat

Each mode has a corresponding script in the ./src directory of the form 

```
container-{lower-case-mode}.sh
```

Adding or modifying the provided modes should be done in consultation with the devops team. Suggestions welcome as PRs.

## Environment variable contract

The application is expected to receive all its configuration via environment variables. This permits it to run equally well locally, in a docker container or as AWS Lambda code.

Variables are divided below into sets, with each set representing particular functionality, the support for which is already present in this repo. If the functionality is optional, the first variable in the set 
is used to detect if the functionality is required.

Variables containing sensitive material can be protected using the AWS KMS encryption service. If encrypted, the ciphertext will be base64 encoded.
All environment variables are thus tested to see if they are base64 encoded, and can be decrypted via AWS KMS. If either step fails, then the value
is used as is. This logic permits local testing with plaintext values and storage of environment values in config repos without risk of exposure.

If there is a discrepancy between a project/product and this repo, align to what is documented below. If it seems wrong, prepare a PR.

### Run mode for codeontap

```
# Run as a web application
APP_RUN_MODE="WEB"
APP_WORKER_COUNT="3"
#
# Use manage.py to run one or more run-to-completion tasks
APP_RUN_MODE="TASK"
#
# Run as a celery worker
#
APP_RUN_MODE="WORKER"
APP_WORKER_COUNT="3"
```

### Basic django settings

```
DJANGO_DEBUG=True
DJANGO_SECRET_KEY=
```

If debug is false, then a value must be provided for DJANGO_SECRET_KEY.

### SQL Database

```
DATABASE_HOST=
DATABASE_PORT=
DATABASE_NAME=
DATABASE_USERNAME=
DATABASE_PASSWORD=
#
# This is optional - defaults to postgresql
DATABASE_ENGINE=
```

### RabbitMQ

```
RABBITMQ_HOST=
RABBITMQ_PORT=
RABBITMQ_VHOST=
RABBITMQ_USERNAME=
RABBITMQ_PASSWORD=
```

### Redis session caching

```
SESSION_REDIS_HOST=
SESSION_REDIS_PORT=
SESSION_REDIS_DB=
```

### Redis general caching

```
CACHE_REDIS_HOST=
CACHE_REDIS_PORT=
CACHE_REDIS_DB=
```

### CouchDB

```
COUCHDB_USERNAME=
COUCHDB_PASSWORD=
```

### Sentry

```
SENTRY_DSN=
```


### Local development (TODO: review/update)

You can start either docker-composed environment (with postgres and stuff) or start things locally. Shared deployments described in "Devops" section. All instructions assume you already in the repo root.

#### docker-compose way

It doesn't work yet.

    $ cp local-docker-compose.env.sample local-docker-compose.env
    $ sudo docker-compose up

and navigate to the port from docker-compose file (http://127.0.0.1:8888/ by default). Yoy may not need sudo if you have docker configured accordingly, but that's another story.

Copy ``local-classic.env.example`` to ``.env`` and change it with your local environment settings.

#### Old-style way

If you prefer old-style way without docker overhead. Please ensure you have all requirements configured (currently it's just database, so you need some postgres installation).
`python3.6 -m venv .venv` shall create Python 3 virtualenv (expected python3.6). Virtualenv directory may have any name, just please don't commit it (env and .venv are gitignored already).

Please note that before first manage.py command you have to export some env variables, otherwise default will be used. In most cases you have to copy `local-classic.env.example` file to `.env` file and update it (database, debug etc.). Python code has some hook which tries to read this file every time (yet, may be we remove it).

    $ pyvenv .venv
    $ source .venv/bin/activate
    $ pip install pip --upgrade
    $ pip install -r requirements.txt
    $ ./manage.py check
    $ ./manage.py migrate
    $ ./manage.py createsuperuser
    $ ./manage.py runserver

Another approach is to keep virtualenv outside the working directory, so just create it somewhere else and use the same way.

After that navigate to the correct place (runserver shows where exactly, by default http://localhost:8000/ but you can change the port).

TODO: describe how to run celery and so on (when we have it).

### Production Deployment

This section is completely for Dockerfile debug.

To test if this will work remotely without need to push it to Jenkins and wait. Michael, have fun and delete that section.
It creates some postgres and some standard container, postgres just for convenience - so you don't have to have any RDS installation. You can put existing in env files if you have one.

    $ cp deploy/docker-compose-way/prod-docker-compose.env.sample ./prod-docker-compose.env
    $ cp deploy/docker-compose-way/prod-docker-compose.yml ./prod-docker-compose.yml
    $ docker-compose -f prod-docker-compose.yml up

Expect it hangs and show you logs from nginx and django.

To go inside the container `docker-compose -f prod-docker-compose.yml exec web bash`
Then you can create database and so on:

    $ cd /app/src/
    $ ./manage.py check
    $ ./manage.py migrate
    $ ./manage.py createsuperuser

When you are finished press control-c in that hanged console and then:

    $ docker-compose -f prod-docker-compose.yml down

Please do not commit it.
It's going to use dockerfile defined in this file (Dockerfile), so if you move it then feel free to update yaml file.
If you change anything except ./src/ folder you have to rebuild the containers; if you change ./src/ content then you have just to restart it (check volumes section in yaml file). Env files - also, just restart.
