from django.conf import settings
from django.db import models

from apps.poll.models import Poll


# Create your models here.

class PollResolved(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    poll = models.ForeignKey(
        Poll,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "poll_resolved"
