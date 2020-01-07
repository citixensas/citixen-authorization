#!/usr/bin/env bash
docker-compose -f develop.yml run --rm corexen_develop.django python manage.py makemigrations
