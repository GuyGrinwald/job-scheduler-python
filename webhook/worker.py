import logging
import os

import requests
from celery import Celery

from utils.url_sanitizer import get_base_url

logger = logging.getLogger(__name__)

ALLOW_REDIRECTS = os.environ.get("ALLOW_REDIRECTS", False)
ALLOW_REDIRECTS = True if ALLOW_REDIRECTS in {"True", "true"} else False

WEBHOOK_TIMEOUT = int(os.environ.get("WEBHOOK_TIMEOUT", 3))
BROKER_CONNECTION = os.environ.get("BROKER_CONNECTION", "pyamqp://guest@localhost:5672")
BACKEND_CONNECTION = os.environ.get("BACKEND_CONNECTION", "redis://localhost:6379/0")

app = Celery(
    "worker",
    broker=BROKER_CONNECTION,
    backend=BACKEND_CONNECTION,
)


@app.task(name="webhook")
def post_to_url(job_id: int, url: str) -> None:
    """
    Calls the given URL with an added param of the job_id
    """
    webhookurl = _build_webhook_url(job_id, url)
    logger.debug(f"Executing webhook call to {webhookurl}")

    try:
        requests.post(
            webhookurl,
            data={},
            allow_redirects=ALLOW_REDIRECTS,
            timeout=WEBHOOK_TIMEOUT,
        )
        logger.debug(f"Posted to webhook: {webhookurl}")
    except Exception as e:
        logger.exception(f"Failed to post a webhook to {webhookurl}", e)
        return -1
    return 0


@staticmethod
def _build_webhook_url(job_id: int, url: str) -> str:
    """
    Builds a webhook from the given url and job id to the format of {schema}://{host}/{path}/{job_id}
    """
    base_url = get_base_url(url)
    return f"{base_url}/{job_id}" if base_url[-1] != "/" else f"{base_url}{job_id}"
