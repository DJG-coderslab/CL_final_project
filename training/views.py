
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.mixins import AccessMixin, LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import Group
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import generic, View

from training.models import Answer, Question, Quiz, Result
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

class Tmp(AppLoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        logged_employee = request.user
        employee = User.objects.get(username=logged_employee)
        quiz = employee.quiz_set.filter(is_active=True)[0]
        questions = quiz.question_set.all()
        paginator = Paginator(questions, 1)
        page = request.GET.get('page')
        questions = paginator.get_page(page)
        context = {
            'questions': questions,
        }
        return render(request, 'training/question.html', context=context)
    
    def post(self, request, *args, **kwargs):
        context = {}
        return render(request, 'training/question.html', context=context)


# class Tmp(AppLoginRequiredMixin, generic.ListView):
   
    # context_object_name = 'questions'
    # paginate_by = 1
    # template_name = 'training/question.html'
    #
    # def get_queryset(self):
    #     u = self.request.user.username
    #     user = User.objects.get(username=u)
    #     quiz = user.quiz_set.filter(is_active=True)[0]
    #     questions = quiz.question_set.all()
    #     queryset = questions
    #     # breakpoint()
    #     return queryset


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
