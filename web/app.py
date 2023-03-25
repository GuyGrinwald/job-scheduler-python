from flask import Flask
from flask_restful import Api
from resources.health import Health
from resources.schedule import Schedule
from resources.scheduler import Scheduler

from db.jobs import PersistantDB

app = Flask(__name__)
api = Api(app)

db = PersistantDB()

api.add_resource(Health, "/health")
api.add_resource(Scheduler, "/timers", resource_class_kwargs={"db": db})
api.add_resource(Schedule, "/timers/<int:job_id>", resource_class_kwargs={"db": db})


if __name__ == "__main__":
    # Use this in non-prod envs only
    app.run(debug=False)
