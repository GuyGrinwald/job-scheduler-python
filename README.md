Job Scheduler Python
========================

This is an example Flask web server backed by Postgres and Celery that is able to schedule API calling tasks.

## Assumptions When Building the App
1. It's only possible to schedule future tasks i.e. negative `hours`, `minutes`, and `seconds` are not allowed
2. If a job's scheduled execution time has passed, `get_times` would return 0 instead of a negative number
3. Our API is premissive and casts any non `int` number into an `int` but we don't convert 0.5 hours into 30 minutes

## Prerequisits Before Running the Project

1. If not already present, install Python 3.11 and [virtualeenvwrapper](https://pypi.org/project/virtualenvwrapper/)
2. Create a local virtualenv
```
$ mkvirtualenv {your-env-name}
```
3. Install project dependencies using
```bash
$ pip install -r requirements.txt
```
4. Install [Docker](https://docs.docker.com/get-docker/)
5. Install/Enable [K8s and kubectl](https://kubernetes.io/docs/tasks/tools/)

## Running the App

### Executing Tests

We use [nox](https://nox.thea.codes/en/stable/tutorial.html#running-nox-for-the-first-time) as our testing framework. To run the tests do the following:
1. Install `nox` (comes in the project's `requirements.txt`)
```bash
$ pip install nox
```
2. Run `nox` a nox session e.g. `unit_test`. `nox` will then execute all tests in the given session.
```bash
$ nox --session unit_test -f noxfile.py
```

### Running Using Vanilla Docker
1. Make sure you have `Docker` installed
2. `cd` to the project's root folder
2. Build the `job-scheduler-web` image
```bash
$ docker build -t job-scheduler-web -f web/Dockerfile .
```
3. Build the `job-scheduler-worker` image
```bash
$ docker build -t celery-worker -f webhook/Dockerfile .
```
4. Run the K8s deployment
```bash
$ kubectl apply -f k8s/deployment.yaml
```
5. Run the DB migrations
```bash
$ python manage.py migrate
```
6. You can now access the API via `POST http:localhost:5000/set_timer` or `GET http:localhost:5000:get_times/{task-id}`
7. To kill the containers and clean up resources run
```bash
kubectl delete namespace job-scheduler-namespace
```

## Feature Backlog
