from django.db import models

# Create your models here.



class Log(models.Model):
    datm_insert = models.DateTimeField(null=True)
    datm_update = models.DateTimeField(null=True)
    datm_delete = models.DateTimeField(null=True)
    status = models.BooleanField(null=True)

    class Meta:
        abstract = True