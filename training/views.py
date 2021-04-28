from django.shortcuts import render
from django.views import View

# from training.forms import QuestionForm
# Create your views here.

from training.forms import UserRegisterForm

class Tmp(View):
    def get(self, request, *args, **kwargs):
        context = {
            'form': UserRegisterForm()
        }
        return render(request, 'training/tmp.html', context=context)