
from collections import defaultdict

from django.core.paginator import Paginator
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.mixins import AccessMixin, LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import Group
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import generic, View

from training.models import Answer, Question, Quiz, Result, ResultAnswer
from training.setup import QUESTIONS_IN_QUIZ
# from training.forms import QuestionForm
# Create your views here.

from training.forms import UserRegisterForm

User = get_user_model()


class AppLoginRequiredMixin(LoginRequiredMixin):
    """Settings for application"""
    # TODO Tylko czy to jest prawidłowe działanie? Czy można bezkarnie
    #  nadpisywac klasę jak metodę?
    #  Jednak nie, lepiej używać swoich nazw, bo po czasie będzie problem,
    #  gdzie szukać, nie będzie jednoznaczności
    login_url = reverse_lazy('tr:register')
    permission_denied_message = "Trzeba się zarejestrować!"


class OneQuestionView(AppLoginRequiredMixin, View):
   
    def __init__(self, *args, **kwargs):
        self.employee = None
        self.quiz = None
        self.paginator = None
        self.current_question = None
        self.page = None
        super().__init__(*args, **kwargs)
    
    def setup_setting(self, request):
        self.employee = User.objects.get(username=request.user)
        self.quiz = self.employee.quiz_set.get(is_active=True)
        self.paginator = self.prepare_paginator()
        self.page = request.session.get('question_number')
        current_obj = self.paginator.get_page(self.page)[0]
        self.current_question = Question.objects.get(id=current_obj.get('id'))
    
    def prepare_paginator(self):
        questions = self.prepare_questions()
        paginator = Paginator(questions, 1)
        return paginator
    
    def write_answer(self, request):
        answer_id = request.POST.get('employee_choice')
        if answer_id:
            result = Result.objects.get(quiz=self.quiz)
            for answer in self.current_question.answer_set.all():
                obj = result.resultanswer_set.get(answer=answer)
                obj.employee_answer = False
                obj.save()
            result_answer = result.resultanswer_set.get(answer=answer_id)
            result_answer.employee_answer = True
            result_answer.save()
    
    def get(self, request, *args, **kwargs):
        self.setup_setting(request)
        page = request.GET.get('page')
        questions = self.paginator.get_page(page)
        request.session['question_number'] = page
        context = {'questions': questions}
        return render(request, 'training/question.html', context=context)
    
    def post(self, request, *args, **kwargs):
        self.setup_setting(request)
        self.write_answer(request)
        if request.POST.get('answer_button'):
            self.paginator = self.prepare_paginator()   # trzeba odświeżyć paginator po zapisie do DB
            page = str(int(self.page) + 1)
            pgn = self.paginator
            page = pgn.num_pages if int(page) > pgn.num_pages else page
            questions = self.paginator.get_page(page)
            request.session['question_number'] = page
            context = {'questions': questions}
            return render(request, 'training/question.html', context=context)
        elif request.POST.get('end_button'):
            scores = 0
            max_points = 0
            result = Result.objects.get(quiz=self.quiz)
            for question in self.quiz.question_set.all():
                max_points += question.points
                for answer in question.answer_set.all():
                    is_correct = answer.is_correct
                    employee_answer = answer.resultanswer_set.get(result=result).employee_answer
                    if is_correct and employee_answer:
                        print(f"=== OK ===")
                        scores += question.points
            context = {
                'scores': scores,
                'max_points': max_points
            }
            return render(request, 'training/summary.html', context=context)
        else:
            return render(request, 'training/tmp.html')

    def prepare_questions(self):
        questions = []
        for question in self.quiz.question_set.all():
            questions_dict = {}
            questions_dict['id'] = question.id
            questions_dict['content'] = question.content
            answers = []
            for answer in question.answer_set.all():
                answers_dict = {}
                answers_dict['id'] = answer.id
                answers_dict['content'] = answer.content
                answers_dict['choice'] = self.quiz.result_set.first().resultanswer_set.get(answer=answer).employee_answer
                answers.append(answers_dict)
            questions_dict['answers'] = answers
            questions.append(questions_dict)
        return questions


class Tmp(AppLoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        context = {
            'questions': ['nic']
        }
        return render(request, 'training/tmp.html', context=context)


class TmpLogout(View):
    def get(self, request):
        # breakpoint()
        logout(request)
        # breakpoint()
        return render(request, 'training/__base__.html')


class OkView(View):
    """class only for test, to remove later"""
    def get(self, request):
        print("OkView")
        # breakpoint()
        return render(request, 'training/__base__.html')
    
    
class RegisterUserView(generic.FormView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('tr:ok')
    template_name = 'training/register.html'

    @staticmethod
    def _create_quiz(employee=None):
        """Creating quiz per user"""
        questions = set()
        while len(questions) < QUESTIONS_IN_QUIZ:
            questions.add(Question.objects.all().order_by('?').first())
        result_object = Result.objects.create()
        quiz_object = Quiz.objects.create()
        quiz_name = (f"{employee.last_name}_{employee.first_name}_"
                     f"{quiz_object.date.strftime('%Y-%m-%d')}")
        quiz_object.name = quiz_name
        quiz_object.is_active = True
        quiz_object.save()
        quiz_object.user.add(employee)
        result_object.user.add(employee)
        result_object.quiz.add(quiz_object)
        for question in questions:
            quiz_object.question_set.add(question)
            for answer in question.answer_set.all():
                result_object.answer.add(answer)

    def form_valid(self, form):
        cd = form.cleaned_data
        employee, _ = User.objects.update_or_create(
            username=cd.get('username'),
            defaults=cd
        )
        employee.last_login = timezone.now()
        employee.save()
        Group.objects.get(name='employees').user_set.add(employee)
        new_quiz = True
        today = timezone.datetime.today().strftime('%Y-%m-%d')
        for quiz in employee.quiz_set.all():
            if quiz.is_active:
                if today == quiz.date.strftime('%Y-%m-%d'):
                    new_quiz = False
                else:
                    quiz.is_active = False
                    quiz.save()
        if new_quiz:
            self._create_quiz(employee=employee)
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


class QuestionView(generic.ListView):
    pass
