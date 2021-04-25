from django.shortcuts import render
from django.views import View

from training.forms import QuestionForm
# Create your views here.


class Tmp(View):
    def get(self, request, *args, **kwargs):
        context = {
            'form': QuestionForm
        }
        return render(request, 'training/tmp.html', context=context)
    
    def post(self, request, *args, **kwargs):
        form = QuestionForm(request.POST)

        context = {
            'form': form
        }
        # breakpoint()
        if form.is_valid():
            context = {
                'form': form
            }
            return render(request, 'training/tmp.html', context=context)
        return render(request, 'training/tmp.html', context=context)
