FROM python:3.6-alpine

ENV PYTHONUNBUFFERED 1

RUN apk update \
  # dependencies
  && apk add --virtual build-deps gcc python3-dev musl-dev \
  # psycopg2 dependencies
  && apk add --virtual build-deps gcc python3-dev musl-dev \
  && apk add postgresql-dev \
  # Pillow dependencies
  && apk add jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev \
  # Translations dependencies
  && apk add gettext

# Requirements are installed here to ensure they will be cached.
COPY ./requirements /requirements
RUN pip install -r /requirements/requirements-dev.txt

WORKDIR /app
