from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic, View

# from training.forms import QuestionForm
# Create your views here.

from training.forms import UserRegisterForm

User = get_user_model()


class Tmp(View):
    def get(self, request, *args, **kwargs):
        context = {
            'form': UserRegisterForm()
        }
        return render(request, 'training/__base__.html', context=context)
    
    
class RegisterUserView(generic.CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('tr:tmp')
    print(f"reverse: {reverse_lazy}")
    template_name = 'training/tmp.html'
    
    def form_valid(self, form):
        # breakpoint()
        return super().form_valid(form)
        