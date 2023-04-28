from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class QA(models.Model):
    question = models.CharField(max_length=200)
    answer = models.CharField(max_length=2, choices=[('SI', 'SI'), ('NO', 'NO')])
    answered_correctly = models.BooleanField(default=False)

    def __str__(self):
        return self.question

class UserAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(QA, on_delete=models.CASCADE)
    answered_correctly = models.BooleanField(default=False)
