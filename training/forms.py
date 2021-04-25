
from django import forms

from training.models import Question


class QuestionForm(forms.ModelForm):
    
    class Meta:
        model = Question
        fields = ('content', 'points',)
    
    ans1 = forms.CharField(max_length=255, empty_value=True)
    ans2 = forms.CharField(max_length=255, empty_value=True)
    ans3 = forms.CharField(max_length=255, empty_value=True)
    ans4 = forms.CharField(max_length=255, empty_value=True)
    ans5 = forms.CharField(max_length=255, empty_value=True)
    ans6 = forms.CharField(max_length=255, empty_value=True)


