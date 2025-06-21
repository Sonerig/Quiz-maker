from django.db import models, transaction
from django.contrib.auth.models import AbstractUser, Group
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.contrib.auth.hashers import make_password


class Class(models.Model):
    class_name = models.CharField(max_length=5, verbose_name="Название класса")

    class Meta:
        verbose_name = "Класс"
        verbose_name_plural = "Классы"

    def __str__(self):
        return self.class_name

class CustomUser(AbstractUser):
    classID = models.ForeignKey(Class, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Класс")
@receiver(pre_save, sender=CustomUser)
def hash_password(sender, instance, **kwargs):
    if not instance.password.startswith('pbkdf2_sha256$'):
        instance.password = make_password(instance.password)
    
@receiver(post_save, sender=CustomUser)
def assign_default_group(sender, instance, created, **kwargs):
    if created and not instance.is_staff and not instance.groups.exists():
        def on_commit():
            instance.groups.set([Group.objects.get(name='Ученик')])
        transaction.on_commit(on_commit)

class Journal(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="Ученик")
    score = models.FloatField(verbose_name="Оценка")
    questions_count = models.IntegerField(verbose_name="Общее количество вопросов")
    datetime = models.DateTimeField(verbose_name="Дата и время прохождения теста")
    
    def percentage(self):
        if self.questions_count > 0:
            return (self.score / self.questions_count) * 100
        return 0

    class Meta:
        verbose_name = "Запись"
        verbose_name_plural = "Журнал"