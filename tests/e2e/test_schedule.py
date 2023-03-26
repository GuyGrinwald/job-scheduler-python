import logging

import pytest
import requests
from pytest_bdd import given, scenario, then, when

import django  # isort: skip

logger = logging.getLogger(__name__)

try:
    # sets up the db connection
    django.setup()
except Exception as e:
    logger.exception("Unable to load Django, db will not be available")
    raise e

from db.timer.models import Job  # isort: skip


@scenario("schedule.feature", "Getting the time until a job is executed")
def test_schedule():
    pass


@given("I scheduled a job", target_fixture="test_job")
def schedule_job():
    logger.info(f"Creating job")
    test_job = Job.objects.create(
        hours=0, minutes=0, seconds=30, url="https://www.google.com"
    )
    logger.info(f"Job created: {test_job}")

    # Return results as a fixture
    yield test_job

    # Cleanup
    try:
        test_job.delete()
    except Exception as e:
        logger.warning(f"Unable to clean job {test_job.id} after tests", e)


@when("I make a GET call to the timer API", target_fixture="api_resp")
def get_schedule(test_job):
    logger.info(f"testing job {test_job}")
    resp = requests.get(f"http://localhost:5000/timers/{test_job.id}", timeout=5)
    return resp


@then("I should get the estimated time until execution")
def timer_is_valid(api_resp):
    logger.info(f"testing response {api_resp}")
    time_left = api_resp.json().get("time_left", 0)
    assert time_left >= 29 and time_left <= 30
