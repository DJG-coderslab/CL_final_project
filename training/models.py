import uuid

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models

User = settings.AUTH_USER_MODEL


class Quiz(models.Model):
    """
    class for Quiz objects
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateTimeField(auto_now_add=True, null=True)
    is_active = models.BooleanField(default=False)
    name = models.CharField(max_length=255)
    user = models.ManyToManyField(User)
    
    def __str__(self):
        return str(self.name)
    

class Question(models.Model):
    """
    class for Question objects
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content = models.CharField(max_length=255)
    quiz = models.ManyToManyField(Quiz)
    points = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return str(self.content)


class Answer(models.Model):
    """
    class for Answer objects
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE,
                                 null=True)
    
    def __str__(self):
        return str(self.content)


class Result(models.Model):
    """There are the reference to the answer of employee"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ManyToManyField(User)
    quiz = models.ManyToManyField(Quiz)
    answer = models.ManyToManyField(Answer, through='ResultAnswer')


class ResultAnswer(models.Model):
    result = models.ForeignKey(Result, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    employee_answer = models.BooleanField(default=False)


class QuizDomain(models.Model):
    name = models.CharField(max_length=255, null=True)
    description = models.TextField(null=True)
    manual = models.TextField(null=True)
