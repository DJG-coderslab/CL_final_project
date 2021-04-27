from django.shortcuts import render
from django.views import View

# from training.forms import
from training.models import Question


class Tmp(View):
    def get(self, request, *args, **kwargs):
        questions = Question.objects.all().order_by('?').first()
        context = {
            'question': questions,
        }
        return render(request, 'training/tmp.html', context=context)