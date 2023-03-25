from datetime import timedelta

from django.core.validators import MinValueValidator
from django.db import models

JOB_STATUS = (
    (0, "Pending"),
    (1, "Success"),
    (2, "Failed"),
)


class Job(models.Model):
    """
    A data class that represent a row in the DB
    """

    hours = models.IntegerField(validators=[MinValueValidator(0)])
    minutes = models.IntegerField(validators=[MinValueValidator(0)])
    seconds = models.IntegerField(validators=[MinValueValidator(0)])
    url = models.URLField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=JOB_STATUS)

    @property
    def schedule(self):
        "Returns the date and time of the schedule"
        return self.created + timedelta(
            hours=self.hours, minutes=self.minutes, seconds=self.seconds
        )
