from django.contrib.auth import get_user_model
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


class Tmp(View):
    def get(self, request, *args, **kwargs):
        context = {
            'form': UserRegisterForm()
        }
        return render(request, 'training/__base__.html', context=context)
    
    
class RegisterUserView(generic.FormView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('tr:tmp')
    template_name = 'training/tmp.html'

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
        quiz_object.save()
        quiz_object.user.add(employee)
        result_object.user.add(employee)
        result_object.quiz.add(quiz_object)
        for question in questions:
            quiz_object.question_set.add(question)
            for answer in question.answer_set.all():
                result_object.answer.add(answer)

    def form_valid(self, form):
        # TODO
        #  wyzwolić procedurę losowania pytań
        cd = form.cleaned_data
        employee, _ = User.objects.update_or_create(
            username=cd.get('username'),
            defaults=cd
        )
        employee.last_login = timezone.now()
        employee.save()
        Group.objects.get(name='employees').user_set.add(employee)
        self._create_quiz(employee=employee)
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

