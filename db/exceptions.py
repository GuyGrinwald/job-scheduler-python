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


class IllegalJobStatusError(DBError):
    def __init__(self, job_status: int) -> None:
        self.job_status = job_status
        super().__init__(
            message=f"Job status {job_status} is not allowed. Must be one of [0, 1, 2]."
        )
