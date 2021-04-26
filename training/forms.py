
from django import forms
from django.core.exceptions import ValidationError

from training.models import Answer, Question


class AnswerForm(forms.ModelForm):
    """Form for Answer model, using in admin panel"""
    class Meta:
        model = Answer
        fields = ['content', 'is_correct']


class QuestionF(forms.ModelForm):
    """form for Question, using in admin panel"""
    class Meta:
        model = Question
        fields = ['content', 'points']

