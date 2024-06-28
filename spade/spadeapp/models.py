from django.db import models

# Create your models here.
class SampleModel(models.Model):
    fieldSample = models.CharField(max_length=10)

    def __str__(self):
        return self.fieldSample
