
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.mixins import AccessMixin, LoginRequiredMixin
from django.contrib.auth.models import Group
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import generic, View

from training.models import Question, Quiz, Result, QuizDomain
from training.setup import PASS_RATE, QUESTIONS_IN_QUIZ
# from training.forms import QuestionForm

from training.forms import UserRegisterForm
from training import business_logic as bl

User = get_user_model()


class StartView(View):
    """View for first page of application"""
    def get(self, request, *args, **kwargs):
        qd = QuizDomain.objects.first()
        context = {
            'description': qd.description,
            'manual': qd.manual
        }
        return render(request, 'training/start.html', context=context)


class IsActiveQuizMixin:
    """Mixin for checking if particular Quiz is active"""
    def dispatch(self, request, *args, **kwargs):
        employee = request.user
        quiz = employee.quiz_set.all().order_by('date').last()
        if quiz.is_active:
            resp = super().dispatch(request, *args, **kwargs)
            return resp
        else:
            context = {'error': 'Quiz nie jest już aktywny!'}
            return render(request, 'training/error.html', context=context)


class AppLoginRequiredMixin(LoginRequiredMixin):
    """Settings for application"""
    login_url = reverse_lazy('tr:register')
    permission_denied_message = "Trzeba się zarejestrować!"


class QuestionView(bl.Question, View):
    """Parent class with common settings and methods"""
    def setup_setting(self, request):
        """settings for Views"""
        self.employee = request.user
        self.quiz = self.employee.quiz_set.all().order_by('date').last()
        self.paginator = self.prepare_paginator(self.prepare_questions)
        self.page = request.session.get('question_number')
        current_obj = self.paginator.get_page(self.page)[0]
        self.current_question = Question.objects.get(id=current_obj.get('id'))

    def prepare_paginator(self, fn):
        """Parameters for paginator
            
            the fn there is a function for creating question's list
        """
        questions = fn()
        paginator = Paginator(questions, 1)
        return paginator


class OneQuestionView(AppLoginRequiredMixin, IsActiveQuizMixin, QuestionView):
    """The view with question for which the employee need to answer"""
    
    def get(self, request, *args, **kwargs):
        self.setup_setting(request)
        page = request.GET.get('page') or 1
        questions = self.paginator.get_page(page)
        request.session['question_number'] = page
        context = {'questions': questions, 'practice_title': self.quiz.id}
        return render(request, 'training/question.html', context=context)
    
    def post(self, request, *args, **kwargs):
        self.setup_setting(request)
        self.write_answer(request)
        if request.POST.get('answer_button'):
            self.paginator = self.prepare_paginator(self.prepare_questions)   # trzeba odświeżyć paginator po zapisie do DB
            page = str(int(self.page) + 1)
            pgn = self.paginator
            page = pgn.num_pages if int(page) > pgn.num_pages else page
            questions = self.paginator.get_page(page)
            request.session['question_number'] = page
            context = {'questions': questions}
            return render(request, 'training/question.html', context=context)
        else:
            return render(request, 'training/tmp.html')


class QuizSummaryView(AppLoginRequiredMixin, bl.QuizSummary, QuestionView):
    """The view with summary and questions with marked answer which is correct
       and employee's answer"""
    # TODO QuizSummary...

    def get(self, request, *args, **kwargs):
        self.setup_setting(request)
        context = self._prepare_summary(request)
        return render(request, 'training/summary.html',
                      context=context)
    
    def post(self, request, *args, **kwargs):
        self.setup_setting(request)
        self.quiz.is_active = False
        self.quiz.save()
        context = self._prepare_summary(request)
        return render(request, 'training/summary.html', context=context)


class RegisterUserView(bl.Register, generic.FormView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('tr:one-question')
    template_name = 'training/register.html'

    def form_valid(self, form):
        cd = form.cleaned_data
        employee = self.handle_register_data(form_data=cd)
        login(self.request, employee)
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            try:
                User.objects.get(
                    username=request.POST.get('username'))
                form.cleaned_data['username'] = request.POST['username']
                return self.form_valid(form)
            # TODO do poprawy
            #  brzydki sposób, ale rozwiązuje podstawowy problem jak w
            #  formularzu na bazie modelu obejść ograniczenia unikalności
            #  klucza? Może będzie trzeba zrobić swój formularz?
            except User.DoesNotExist:
                return self.form_valid(form)


class Tmp(AppLoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        context = {
            'questions': ['nic']
        }
        return render(request, 'training/tmp.html', context=context)


class TmpLogout(View):
    def get(self, request):
        logout(request)
        return render(request, 'training/base.html')


class OkView(View):
    """class only for test, to remove later"""
    
    def get(self, request):
        print("OkView")
        return render(request, 'training/base.html')


