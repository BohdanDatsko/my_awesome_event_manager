# My Awesome Event Manager

Behold My Awesome Event Manager!

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

License: MIT

## Settings

Moved to [settings](http://cookiecutter-django.readthedocs.io/en/latest/settings.html).

## Basic Commands

### Starting the Project
at first be sure that you have installed docker and docker-compose on your machine.
Then you need to stop your local postgresql service if you have it running on your machine.

    $ make up

or

    $ docker compose -f docker-compose.local.yml up

### Setting Up Your Users

- To create a **superuser account**, use this command:

      $ make createsuperuser
    or

        $ docker compose -f docker-compose.local.yml run --rm django python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

### Test coverage

To run the tests, check your test coverage, and generate an HTML coverage report:

    $ make coverage_html
or

    $ docker compose -f docker-compose.local.yml run --rm django coverage run -m pytest
    $ docker compose -f docker-compose.local.yml run --rm django coverage html
    $ docker compose -f docker-compose.local.yml run --rm django open htmlcov/index.html

#### Running tests with pytest

    $ make pytest

## Deployment

The following details how to deploy this application.

### Docker

See detailed [cookiecutter-django Docker documentation](http://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html).
