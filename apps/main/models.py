from django.db import models


class CountData(models.Model):
    count = models.IntegerField(
        'カウンタ',
        default=0,
        null=False,
        blank=False,
    )
