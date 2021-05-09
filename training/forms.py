
from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from training.models import Answer, Question


User = get_user_model()

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


class UserRegisterForm(forms.ModelForm):
    """Based by auth.user form to register employee"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = '8000511'
        self.fields['username'].help_text = ""
        self.fields['first_name'].widget.attrs['placeholder'] = 'Jan'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Nowak'
       
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name',)
        labels = {
            'username': 'numer pracownika',
            'first_name': 'imię',
            'last_name': 'nazwisko'
        }
