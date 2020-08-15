from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Test(models.Model):
    title = models.CharField(max_length=120)

    def __str__(self):
        return self.title


class Question(models.Model):
    text = models.TextField()
    test = models.ForeignKey(Test, on_delete=models.CASCADE)

    def __str__(self):
        return self.text


class Answer(models.Model):
    text = models.TextField()
    is_correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return self.text


class Result(models.Model):
    count_questions = models.IntegerField()
    count_correct_questions = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    attempt = models.IntegerField()
