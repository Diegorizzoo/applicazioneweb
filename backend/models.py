from django.db import models

class QA(models.Model):
    question = models.CharField(max_length=200)
    answer = models.CharField(max_length=2, choices=[('SI', 'SI'), ('NO', 'NO')])
    answered_correctly = models.BooleanField(default=False)

    def __str__(self):
        return self.question

