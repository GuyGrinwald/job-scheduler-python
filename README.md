Job Scheduler Python
========================

This is an example Flask web server backed by Postgres and Celery that is able to schedule API calling tasks.

## Assumptions When Building the App

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
2. `cd` to project root folder and build the `job-scheduler-web` image
```bash
$ docker build -t job-scheduler-web -f web/Dockerfile .
```
3. Run the image with exposed ports (make sure you're binded to the correct localhost - could also be `0.0.0.0`)
```bash
$ docker run --name job-scheduler-web -p 127.0.0.1:5000:5000 -d job-scheduler-web
```
4. Run a celery Docker
```
$
```
5. Run a Postgres Docker
```
$
```
6. `cd` to project root folder and build the `job-scheduler-worker` image
```bash
$ docker build -t job-scheduler-worker -f job_scheduler/Dockerfile .
```
7. Run the image
```bash
$ docker run --name job-scheduler-worker -d job-scheduler-worker
```
8. You can now access the API via `POST http:localhost:5000/set_timer` or `GET http:localhost:5000:get_times/{task-id}`

### Running Using K8s
1. Build the Docker images as instructed in [**Running Using Vanilla Docker**](#Running-Using-Vanilla-Docker)
2. Run the K8s deployment
```bash
$ kubectl apply -f k8s/deployment.yaml
```
3. You can now access the API via `POST http:localhost:5000/set_timer` or `GET http:localhost:5000:get_times/{task-id}`
4. To kill the containers and clean up resources run
```bash
kubectl delete namespace job-scheduler-namespace
```

## Feature Backlog
