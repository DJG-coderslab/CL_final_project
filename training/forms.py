
from django import forms
from django.core.exceptions import ValidationError

from training.models import Answer, Question


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
        if Question.objects.get(content=cd.get('content')).answer_set.count() < 2:
            raise ValidationError("za mało odpowiedzi")

    # filled_answer = 0
        # filled_corrections = 0
        # answers = [cd.get('ans1'), cd.get('ans2'), cd.get('ans3'),
        #            cd.get('ans4'), cd.get('ans5'), cd.get('ans6')]
        # corrects = [cd.get('is_correct1'), cd.get('is_correct2'),
        #             cd.get('is_correct3'), cd.get('is_correct4'),
        #             cd.get('is_correct5'), cd.get('is_correct6')]
        # for ans, corr in zip(answers, corrects):
        #     filled_answer += 1 if ans else 0
        #     filled_corrections += 1 if corr else 0
        #     if not ans and corr:
        #         raise ValidationError("Nie może być samo is_correct")
        # if filled_answer < 3:
        #     raise ValidationError("za mało odpowiedzi")
        # if filled_corrections < 1:
        #     raise ValidationError("minimum jedna poprawna odpowiedź")

    # def save(self, commit=True, *args, **kwargs):
    #     instance = super(QuestionForm, self).save(commit=False, *args, **kwargs)
    #     cd = self.cleaned_data
    #     # if commit:
    #     breakpoint()
    #     # TODO instance to obiekt Question, czyli do instance można dodać
    #     #  pytania z formularzać
    #     #  Pytanie: Jak zrobić update? Może właśnie przez update_or_create?
    #     #  I zamiast .add() zrobić Answer.objects.create(question=instance, ...)
    #
    #     question = Question.objects.update_or_create(
    #         content=cd.get('content'),
    #         points=cd.get('points'),
    #         defaults={
    #             'content': f"OR save: {cd.get('content')}",
    #             'points': cd.get('points')
    #         }
    #     )
    #     breakpoint()
    #     return instance

class AnswerForm(forms.ModelForm):

    class Meta:
        model = Answer
        fields = ['content', 'is_correct']



class QuestionF(forms.ModelForm):

    class Meta:
        model = Question
        fields = ['content', 'points']

    def clean(self):
        cd = super().clean()

        # breakpoint()
        # if Question.objects.get(content=cd.get('content')).answer_set.count() < 4:
        #     raise ValidationError("za mało odpowiedzi")
