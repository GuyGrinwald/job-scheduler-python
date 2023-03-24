from flask import request
from flask_restful import Resource, abort

from db import exceptions as db_excpetions
from db.jobs import JobDB
from web.errors.codes import IILEAGAL_SCHEDULE_ERROR


class Scheduler(Resource):
    """
    A Flask resource that handle scheduling web posting tasks
    """

    def __init__(self, **kwargs) -> None:
        self.db: JobDB = kwargs["db"]
        super().__init__()

    def post(self):
        json_data = request.get_json(force=True)
        hours = json_data.get("hours", 0)
        minutes = json_data.get("minutes", 0)
        seconds = json_data.get("seconds", 0)
        url = json_data.get("url", 0)

        try:
            new_id = self.db.create(hours, minutes, seconds, url)
            return {"id": new_id}
        except db_excpetions.IllegalScheduleError as e:
            abort(IILEAGAL_SCHEDULE_ERROR, description=str(e))
