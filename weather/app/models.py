from datetime import datetime

from django.db import models
from django.core.cache import cache
from django.contrib.postgres.fields import JSONField

from django_extensions.db.models import TimeStampedModel


class WeatherReportHistory(TimeStampedModel):
    location = models.CharField(max_length=125, db_index=True)
    result = JSONField()

    class Meta:
        unique_together = ("location", "created",)

    def __str__(self):
        return self.location

    def save(self, *args, **kwargs):
        super(WeatherReportHistory, self).save(*args, **kwargs)
        # cached result data by location after database operation
        key = "{}_{}".format(self.location, datetime.today().strftime("%d%m%Y"))
        data = dict(location=self.location, result=self.result)
        cache.set(key, data, 3600)
