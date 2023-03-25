from datetime import datetime, timezone

from flask_restful import Resource, abort

from db import exceptions as db_excpetions
from db.jobs import JobDB
from web.errors.codes import JOB_NOT_FOUND_ERROR


class Schedule(Resource):
    """
    A Flask resource that handles retrieving the time until scheduled tasks are executed
    """

    def __init__(self, **kwargs) -> None:
        self.db: JobDB = kwargs["db"]
        super().__init__()

    def get(self, job_id: int):
        try:
            job = self.db.get(job_id)
            next_execution = (job.schedule - datetime.now(timezone.utc)).total_seconds()
            return {"id": job_id, "time_left": max(0, next_execution)}
        except db_excpetions.JobNotFoundError as e:
            abort(JOB_NOT_FOUND_ERROR, description=str(e))
