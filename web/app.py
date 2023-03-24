from flask import Flask
from flask_restful import Api

from resources.health import Health
from resources.schedule import Schedule
from resources.scheduler import Scheduler

app = Flask(__name__)
api = Api(app)

api.add_resource(Health, "/health")
api.add_resource(Scheduler, "/set_timer")
api.add_resource(Schedule, "/<int:job_id>")


if __name__ == "__main__":
    # Use this in non-prod envs only
    app.run(debug=False)
