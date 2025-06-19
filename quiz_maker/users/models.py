from django.db import models
from django.contrib.auth.models import AbstractUser

from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.auth.hashers import make_password


class Class(models.Model):
    class_name = models.CharField(max_length=5)

    def __str__(self):
        return self.class_name

class CustomUser(AbstractUser):
    classID = models.ForeignKey(Class, on_delete=models.CASCADE, blank=True, null=True)
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='CustomUser_groups',
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to.',
    )
@receiver(pre_save, sender=CustomUser)
def hash_password(sender, instance, **kwargs):
    if not instance.password.startswith('pbkdf2_sha256$'):
        instance.password = make_password(instance.password)
