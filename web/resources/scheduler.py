import logging
import os
from typing import Dict

from celery import Celery
from flask import request
from flask_restful import Resource, abort

from db import exceptions as db_excpetions
from db.jobs import Job, JobDB
from utils.url_sanitizer import get_hostname, validate_url
from web.errors.codes import DOS_URL_ERROR, IILEAGAL_SCHEDULE_ERROR, ILLEAGEL_URL_ERROR

logger = logging.getLogger(__name__)

APP_DOMAIN = os.environ.get("APP_DOMAIN", "localhost")
ILLEGAL_DOMAINS = ["localhost", "127.0.0.1", "0.0.0.0"]


class Scheduler(Resource):
    """
    A Flask resource that handle scheduling web posting tasks
    """

    def __init__(self, **kwargs) -> None:
        self.db: JobDB = kwargs["db"]
        self.app = Celery(
            "worker",
            broker="pyamqp://guest@localhost:5672",
            backend="redis://localhost:6379/0",
        )
        super().__init__()

    def post(self):
        json_data = request.get_json(force=True)
        hours, minutes, seconds, url = self.sanitize_request(json_data)

        try:
            job: Job = self.db.create(hours, minutes, seconds, url)
            self.app.send_task(name="webhook", args=(job.id, url))
            return {"id": job.id}
        except db_excpetions.IllegalScheduleError as e:
            abort(IILEAGAL_SCHEDULE_ERROR, description=str(e))

    def sanitize_request(self, schedule_params: Dict):
        """
        Sanitizes and validates the request parameters to match the API docs
        """
        # Handle scheduling data
        try:
            hours = int(schedule_params.get("hours", 0))
            minutes = int(schedule_params.get("minutes", 0))
            seconds = int(schedule_params.get("seconds", 0))
        except ValueError:
            logger.warning(
                f"Recieved scheduling information: hours: {hours}, minutes: {minutes}, seconds: {seconds}"
            )
            abort(
                IILEAGAL_SCHEDULE_ERROR,
                description="Hours, minutes, and seconds must all be non negative integers",
            )

        # Handle URL
        url = schedule_params.get("url", None)
        self._validate_url_param(url)
        return hours, minutes, seconds, url

    def _validate_url_param(self, url: str) -> None:
        """
        Validates that the given URL is legal and our API can handle it

        """
        if not url:
            logger.warning(f"Recieved an empty URL")
            abort(ILLEAGEL_URL_ERROR, description="Missing URL parameter")

        try:
            validate_url(url)
        except ValueError:
            logger.warning(f"Recieved an invalid URL: {url}")
            abort(ILLEAGEL_URL_ERROR, description="The given URL is an invalid format")

        hostname = get_hostname(url)
        if hostname in ILLEGAL_DOMAINS or hostname == APP_DOMAIN:
            logger.warning(f"Recieved an illegal URL")
            abort(DOS_URL_ERROR, description="The given URL is illegal")
