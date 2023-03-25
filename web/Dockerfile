# pull official base image
FROM python:3.11.1-slim-buster

# set work directory
WORKDIR /usr/job_scheduler

# set Python environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install Postgres executalbes
RUN apt-get update -y && apt-get install -y gcc libpq-dev python-dev

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/job_scheduler/requirements.txt
RUN pip install -r requirements.txt

# copy project
COPY ./web /usr/job_scheduler/web
COPY ./utils /usr/job_scheduler/utils
COPY ./db /usr/job_scheduler/db

# set pythonpath
ENV PYTHONPATH "${PYTHONPATH}:/usr/job_scheduler"

# annouce needed ports
EXPOSE 5000

# executes our gunicorn
CMD cd ./web && gunicorn app:app
