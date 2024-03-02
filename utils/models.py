# DJANGO
from django.db import models


class TimeBaseModel(models.Model):
    """     """

    created_on = models.DateTimeField(
        'created at',
        auto_now_add=True,
        help_text='Date time on which the object was created.'
    )

    modified_on = models.DateTimeField(
        'modified at',
        auto_now=True,
        help_text='Date time on which the object was last modified.'
    )

    class Meta:
        abstract = True

        get_latest_by = 'created_on'
        ordering = ['-created_on', '-modified_on']