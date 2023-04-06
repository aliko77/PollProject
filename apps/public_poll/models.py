from django.db import models

# Create your models here.

class PollResolved(models.Model):
    class Meta:
        db_table="poll_resolved"