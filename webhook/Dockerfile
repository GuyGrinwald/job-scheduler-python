# pull official base image
FROM python:3.11.1-slim-buster

# set work directory
WORKDIR /usr/job_scheduler

# set Python environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/job_scheduler/requirements.txt
RUN pip install -r requirements.txt

# copy project
COPY ./webhook /usr/job_scheduler/webhook
COPY ./utils /usr/job_scheduler/utils

# set pythonpath
ENV PYTHONPATH "${PYTHONPATH}:/usr/job_scheduler"

ENTRYPOINT celery -A webhook.worker worker --autoscale 1 --loglevel debug