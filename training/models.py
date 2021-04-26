import uuid

from django.db import models


class Quiz(models.Model):
    """
    class for Quiz objects
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateTimeField(null=True)
    is_active = models.BooleanField(default=False)
    name = models.CharField(max_length=255)
    
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

