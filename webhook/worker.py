import logging

from celery import Celery

logger = logging.getLogger(__name__)


app = Celery(
    "worker",
    broker="pyamqp://guest@localhost:5672",
    backend="redis://localhost:6379/0",
)


@app.task(name="webhook")
def post_to_url(job_id: int, url: str) -> None:
    """
    Calls the given URL with an added param of the job_id
    """
    print("Task Add started")
    print("Task Add done")
    return f"Posted to webhook: {url}/{job_id}"
