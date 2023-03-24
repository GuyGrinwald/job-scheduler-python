from __future__ import annotations  # isort:skip

from abc import ABCMeta, abstractmethod
from datetime import datetime, timedelta
from typing import Dict

from db.exceptions import IllegalScheduleError, JobNotFoundError
from utils.singleton import Singleton


class JobDB:
    __metaclass__ = ABCMeta

    @abstractmethod
    def create(self, hours: int, minutes: int, seconds: int, url: str) -> int:
        """
        Create a new Job object in the DB and returns its id.
        Hours, minutes, and seconds have to be greater than 0
        """
        pass

    @abstractmethod
    def get(self, job_id: str) -> Job:
        """
        Retrieve a job object based on it's id
        """
        pass

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


class InMemoryJobDB(JobDB, Singleton):
    """
    An In-Memory implementation of the JobDB
    """

    def __init__(self):
        super().__init__()
        self.jobs: Dict[int][self.Job] = {}
        self.last_id = 0

    def create(self, hours: int, minutes: int, seconds: int, url: str) -> int:
        if not all(i >= 0 for i in [hours, minutes, seconds]):
            raise IllegalScheduleError()

        self.last_id += 1
        self.jobs[self.last_id] = self.Job(self.last_id, hours, minutes, seconds, url)
        return self.last_id

    def get(self, job_id: str) -> None:
        if job_id not in self.jobs:
            raise JobNotFoundError(job_id)

        return self.jobs[job_id]