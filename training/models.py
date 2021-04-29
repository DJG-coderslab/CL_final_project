import uuid

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


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

