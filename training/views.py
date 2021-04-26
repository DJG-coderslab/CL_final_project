from django.shortcuts import render
from django.views import View

# from training.forms import QuestionForm
from training.models import Question


class Tmp(View):
    def get(self, request, *args, **kwargs):
        context = {
            'question': Question.objects.all().order_by('?').first()
        }
        return render(request, 'training/tmp.html', context=context)