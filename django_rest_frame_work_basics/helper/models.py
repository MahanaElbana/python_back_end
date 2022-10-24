

from django.db import models

class TrackingModel(models.Model):

    created_at = models.DateTimeField(auto_now_add =True)
    updated_at = models.DateTimeField(auto_now =True)

    class Meta :
        ordering = ('-created_at')
        abstract = True