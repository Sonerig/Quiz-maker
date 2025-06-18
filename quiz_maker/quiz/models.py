from django.db import models
from django.conf import settings

# Create your models here.
class Class(models.Model):
    class_name: models.CharField(max_length="5")
    studentID: models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)