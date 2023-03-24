class DBError(Exception):
    "A base class for DB errors"

    def __init__(self, message: str) -> None:
        super().__init__(message)


class IllegalScheduleError(DBError):
    def __init__(self) -> None:
        super().__init__(
            message="Hours, minutes, and seconds have to be greater than 0"
        )


class JobNotFoundError(DBError):
    def __init__(self, job_id: int) -> None:
        self.job_id = job_id
        super().__init__(message=f"Job {job_id} was not found")
