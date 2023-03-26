from __future__ import annotations  # isort:skip
import django  # isort:skip

import logging

logger = logging.getLogger(__name__)

try:
    # sets up the db connection
    django.setup()
except Exception as e:
    logger.exception("Unable to load Django, db will not be available")
    raise e


from abc import ABCMeta, abstractmethod
from datetime import datetime, timedelta
from typing import Dict

from django.core.exceptions import ObjectDoesNotExist
from django.forms import ValidationError

from db.exceptions import (
    DBError,
    IllegalJobStatusError,
    IllegalScheduleError,
    JobNotFoundError,
)
from db.timer.models import Job
from utils.singleton import Singleton


class JobDB:
    __metaclass__ = ABCMeta

    @abstractmethod
    def create(self, hours: int, minutes: int, seconds: int, url: str) -> Job:
        """
        Create a new Job object in the DB and returns its id.
        Hours, minutes, and seconds have to be greater than 0
        """
        pass

    @abstractmethod
    def get(self, job_id: str) -> Job:
        """
        Retrieve a job object based on its id
        """
        pass

    def set_status(self, job_id: str, status) -> None:
        """
        Sets the completion status of a job
        """
        pass


@DeprecationWarning
class InMemoryJobDB(JobDB, Singleton):
    """
    An In-Memory implementation of the JobDB
    """

    class Job:
        """
        A data class that represent a row in the DB
        """

        def __init__(
            self, id: int, hours: int, minutes: int, seconds: int, url: str
        ) -> None:
            self.id = id
            self.hours = hours
            self.minutes = minutes
            self.seconds = seconds
            self.url = url
            self.created = datetime.now()
            self.schedule = self.created + timedelta(
                hours=hours, minutes=minutes, seconds=seconds
            )
            self.status = 0

    ALLOWED_JOB_STATUS = {0, 1, 2}

    def __init__(self):
        super().__init__()
        self.jobs: Dict[int][self.Job] = {}
        self.last_id = 0

    def create(
        self, hours: int, minutes: int, seconds: int, url: str
    ) -> InMemoryJobDB.Job:
        if not all(i >= 0 for i in [hours, minutes, seconds]):
            raise IllegalScheduleError()

        self.last_id += 1
        self.jobs[self.last_id] = self.Job(
            id=self.last_id, hours=hours, minutes=minutes, seconds=seconds, url=url
        )
        return self.jobs[self.last_id]

    def get(self, job_id: str) -> InMemoryJobDB.Job:
        if job_id not in self.jobs:
            raise JobNotFoundError(job_id)

        return self.jobs[job_id]

    def set_status(self, job_id: str, status) -> None:
        if job_id not in self.jobs:
            raise JobNotFoundError(job_id)

        if status not in self.ALLOWED_JOB_STATUS:
            raise IllegalJobStatusError(status)

        self.jobs[job_id].status = status


class PersistantDB(JobDB):
    """
    A Postgres and Django backed implemntation of JobDB
    """

    def __init__(self) -> None:
        super().__init__()

    def create(self, hours: int, minutes: int, seconds: int, url: str) -> Job:
        if not all(i >= 0 for i in [hours, minutes, seconds]):
            raise IllegalScheduleError()

        try:
            job = Job.objects.create(
                hours=hours, minutes=minutes, seconds=seconds, url=url
            )
        except Exception as e:
            logger.exception(
                f"Unable to create job: hours {hours}, minutes {minutes}, seconds {seconds}, url {url}",
                e,
            )
            raise DBError("Unable to create job")

        return job

    def get(self, job_id: str) -> Job:
        try:
            return Job.objects.get(id=job_id)
        except ObjectDoesNotExist:
            raise JobNotFoundError(job_id)
        except Exception as e:
            logger.exception(f"Unable get job {job_id}", e)
            raise DBError(f"Unable to get job {job_id}")

    def set_status(self, job_id: str, status) -> None:
        try:
            job = Job.objects.get(id=job_id)
            job.status = status
            job.full_clean()  # runs model validations
            job.save()
        except ObjectDoesNotExist as e:
            raise JobNotFoundError(job_id)
        except ValidationError as e:
            raise IllegalJobStatusError(status)
        except Exception as e:
            logger.exception(f"Unable to set status {status} to job {job_id}", e)
            raise DBError(f"Unable to set status {status} to job {job_id}")
