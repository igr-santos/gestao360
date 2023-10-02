# Build staticfiles
FROM node:18-alpine AS node-builder

WORKDIR /app

COPY . .

WORKDIR /app/dashboard/tailwindcss

RUN npm i

RUN npm run build

# Use an official Python runtime based on Debian 10 "buster" as a parent image.
FROM python:3.8-slim

# Port used by this container to serve HTTP.
EXPOSE 8000

# Set environment variables.
# 1. Force Python stdout and stderr streams to be unbuffered.
# 2. Set PORT variable that is used by Gunicorn. This should match "EXPOSE"
#    command.
ENV PYTHONUNBUFFERED=1 \
    PORT=8000

# # Install dev libs on system.
# RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
#     build-essential \
#     python3-dev

################## BEGIN INSTALLATION ######################
# Add the packages
# RUN apk add --no-cache python3
# RUN apk add --no-cache --virtual .build-deps py-pip python3-dev musl-dev gcc
RUN apt-get update --yes --quiet
RUN apt-get install --yes --quiet --no-install-recommends build-essential python3-dev
# RUN pip install mysql
# You can skip this step if your Django project has the correct version specified on requirements.txt
#RUN pip install django

# Install the application server.
RUN pip install uwsgi django-storages boto3

# Install the project requirements.
COPY requirements.txt /
RUN pip install -r requirements.txt

# Use /app folder as a directory where the source code is stored.
WORKDIR /app

# Copy the source code of the project into the container.
COPY . .

# Clean up disk space
RUN apt remove  build-essential python3-dev --yes --quiet
# RUN apk del .build-deps python3-dev musl-dev gcc zlib-dev openssl-dev
RUN rm -Rf ~/.cache
##################### INSTALLATION END #####################

# Install the application server.
RUN pip install uwsgi django-storages boto3

# Install the project requirements.
# COPY requirements.txt /
# RUN pip install -r requirements.txt

# Use /app folder as a directory where the source code is stored.
# WORKDIR /app

# Copy the source code of the project into the container.
# COPY . .

COPY --from=node-builder /app .

RUN rm -rf /app/dashboard/tailwindcss

# RUN python manage.py collectstatic --noinput --clear
# --settings project.settings_prod

# Runtime command that executes when "docker run" is called.
CMD ["uwsgi", "--ini", "/app/wsgi.ini"]