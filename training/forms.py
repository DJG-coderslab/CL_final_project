
from django import forms
from django.core.exceptions import ValidationError

from training.models import Question


class QuestionForm(forms.ModelForm):
    
    class Meta:
        model = Question
        fields = ('content', 'points',)
    
    ans1 = forms.CharField(max_length=255, required=False)
    is_correct1 = forms.BooleanField(required=False)
    ans2 = forms.CharField(max_length=255, required=False)
    is_correct2 = forms.BooleanField(required=False)
    ans3 = forms.CharField(max_length=255, required=False)
    is_correct3 = forms.BooleanField(required=False)
    ans4 = forms.CharField(max_length=255, required=False)
    is_correct4 = forms.BooleanField(required=False)
    ans5 = forms.CharField(max_length=255, required=False)
    is_correct5 = forms.BooleanField(required=False)
    ans6 = forms.CharField(max_length=255, required=False)
    is_correct6 = forms.BooleanField(required=False)

    def clean(self):
        cd = super().clean()
        filled_answer = 0
        filled_corrections = 0
        answers = [cd.get('ans1'), cd.get('ans2'), cd.get('ans3'),
                   cd.get('ans4'), cd.get('ans5'), cd.get('ans6')]
        corrects = [cd.get('is_correct1'), cd.get('is_correct2'),
                    cd.get('is_correct3'), cd.get('is_correct4'),
                    cd.get('is_correct5'), cd.get('is_correct6')]
        for ans, corr in zip(answers, corrects):
            filled_answer += 1 if ans else 0
            filled_corrections += 1 if corr else 0
            if not ans and corr:
                raise ValidationError("Nie może być samo is_correct")
        if filled_answer < 3:
            raise ValidationError("za mało odpowiedzi")
        if filled_corrections < 1:
            raise ValidationError("minimum jedna poprawna odpowiedź")
