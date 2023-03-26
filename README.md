Job Scheduler Python
========================

This is an example Flask web server backed by Postgres and Celery that is able to schedule tasks.

## High Level Design

![localImage](./docs/architecture.png)

## Assumptions When Building the App
1. The API accepts JSON formatted payloads for POST requests
2. It's only possible to schedule future tasks i.e. negative `hours`, `minutes`, and `seconds` are not allowed
3. URL is a mandatory paramter and we impose strict validation on it (requireing scheme and netloc). We also only permit up to 200
characters but this can be changed easily
4. Our API is premissive and casts any non `int` number into an `int` but we don't convert 0.5 hours into 30 minutes
5. Since it was not specified explicitly and the example did cover this, I assumed that we append the counter id after 
the path of the URL (and not just the hostname) and we drop other params as they may be inapplicable in that path
6. in `worker.py` I preferd the application to fail if WEBHOOK_TIMEOUT isn't a number since this would make development
and bug triage easier. I also didn't cap this value as this is a developer's configuration and I leave this to their discretion
7. Celery's `eta` feature isn't extermely accurate and can result in some lags in execution. This can be mitigated by tinckering with
some configurations e.g. `worker_timer_precision`
8. I've hard-coded many scalabilty features e.g. Gunicorn's workers and theads, Celery's workers and process and the deployment's replicas. These can be adjusted per our need, or better yet, add auto-scaling

## Prerequisits Before Running the Project

1. If not already present, install Python 3.11 and [virtualeenvwrapper](https://pypi.org/project/virtualenvwrapper/)
2. Create and activate a local virtualenv
```bash
$ mkvirtualenv {your-env-name}
```
3. Add the root of the project to your `PYTHONPATH`
```bash
$ export PYTHONPATH={path-to-root-folder}
```
3. Install project dependencies using
```bash
$ pip install -r requirements.txt
```
4. Install [Docker](https://docs.docker.com/get-docker/)
5. Install/Enable [K8s and kubectl](https://kubernetes.io/docs/tasks/tools/)

## Running the App

### Executing Tests
We use [nox](https://nox.thea.codes/en/stable/tutorial.html#running-nox-for-the-first-time) and `pytest` as our testing framework.

#### Unit Tests
Run `nox` a nox session e.g. `unit_test`. `nox` will then execute all tests in the given session. From the project's root 
directory run the following command
```bash
$ nox -r --session unit_test -f noxfile.py
```

#### E2E Tests
1. Since E2E tests check the full functionality of our app, we need to fully deploy it. Make sure the app is deployed to K8s as described in [Running Using K8s](#running-using-k8s)
2. Set DB connection params (if not done already)
```bash
$ export DJANGO_SETTINGS_MODULE=settings POSTGRES_DB=timer POSTGRES_USER=db_user POSTGRES_PASSWORD=db_password
```
3. Run `nox` a nox session e.g. `e2e_test`. `nox` will then execute all tests in the given session. From the project's root 
directory run the following command
```bash
$ nox -r --session e2e_test -f noxfile.py
```

### Running Using K8s
1. `cd` to the project's root folder
2. Build the `job-scheduler-web` image (from project's root)
```bash
$ docker build -t job-scheduler-web -f web/Dockerfile .
```
3. Build the `job-scheduler-worker` image (from project's root)
```bash
$ docker build -t celery-worker -f webhook/Dockerfile .
```
4. Run the K8s deployment (from project's root)
```bash
$ kubectl apply -f k8s/deployment.yaml
```
5. Run the DB migrations (from project's root)
```bash
$ export DJANGO_SETTINGS_MODULE=settings POSTGRES_DB=timer POSTGRES_USER=db_user POSTGRES_PASSWORD=db_password
$ python db/manage.py migrate
```
6. You can now access the API via `POST http://localhost:5000/timers` or `GET http://localhost:5000:timers/{task-id}`
7. To kill the containers and clean up resources run
```bash
kubectl kubectl config set-context --current --namespace=job-scheduler-namespace
kubectl delete namespace job-scheduler-namespace
kubectl delete pv job-scheduler-pv
```

## Feature Backlog
Given the limited time and scope of the project there are many things I would have wanted to add.
I've listed below the main highlights.

1. Secure credentials for Postgres, RabbitMQ etc.
2. Adding User management, API tokens, rate limiting and quota etc.
3. Adding monitoring, metrics (e.g. failed webhooks, user usage metrics, worker liveliness, API liveliness etc.)
4. Adding tracability from API to Celery workers using GUIDs
5. For production scalability we need to deploy auto-scaling groups for API, Celery, and potentially shard the DB
6. We should also consider moving Celery's broker to be based on SQS or other high-scale platform
7. There's additional logic we can add to make the Celery workers more robust and handle connection issues etc.
8. For ease of development I would add CI and build options so the process isn't so manual
9. I would add many more E2E tests, negative tests, and load tests
10. Much of the application's configs are somewhat hard-coded (e.g. log level etc.). They should be moved to K8s ConfigMaps
11. As with most systems, we would need more documentation 

There are many other features we can think of, but this is of the top of my head ;)

## Troubleshooting
The application was tested on Mac and Windows but things could happen. I tried my best to account for the various
statuses of the testing environment but I wasn't able to account for everything.

### Unable to Run Django Migrations
1. Make sure `DJANGO_SETTINGS_MODULE` is exported and that the `PYTHONPATH` is set to your project's root dir
2. Make sure your virtualenv is enabled
3. Make sure the Postgres container is not resuing an old DB file. This can be seen the logs

### Dockers Not Booting Up
1. K8s deployment can take a few minutes so patience is a virtue.
2. Check the deployment status by running the following commands. There's usually a hint there.
```bash
$ kubectl get deployment job-scheduler-deployment
$ kubeclt describe deployemnt {name-of-deployemnt}
```

### API Isn't Responding or Returning Errors
1. Check you are sending JSON requests
2. Check you are calling the right URL. Some systems are ok with Localhost, and some require `127.0.0.1` etc.