from django.contrib.auth import login, get_user_model
from django.contrib.auth.models import Group
from django.utils import timezone

from training.setup import QUESTIONS_IN_QUIZ, PASS_RATE
from training import models

User = get_user_model()


class Register:
    """class with common methods using in the ordinary views and API views"""
    
    @staticmethod
    def _create_quiz(employee=None):
        """Creating quiz per user creating relevant records in the DB"""
        questions = set()
        while len(questions) < QUESTIONS_IN_QUIZ:
            questions.add(models.Question.objects.all().order_by('?').first())
        result_object = models.Result.objects.create()
        quiz_object = models.Quiz.objects.create()
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
                
    def handle_register_data(self, form_data=None):
        """The form_date is a dictionary with:
            username,
            last_name,
            first_name"""
        cd = form_data
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
        return employee


class Question:
    
    def setup_setting(self, request):
        """settings for Views"""
        self.employee = request.user
        self.quiz = self.employee.quiz_set.all().order_by('date').last()
    
    def prepare_questions(self):
        """Creating list of questions with answers"""
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

    def write_answer(self, request):
        """Writing the answer to DB"""
        answer_id = request.POST.get('employee_choice')
        # Tu walidacja niewiele zmienia. Chodzi tylko o informację, czy ta
        # odpowiedź została zaznaczona przez pracownika. Ten wybór anuluje
        # poprzednie i zawsze jest zero lub jedna wybrana odpowiedź
        if answer_id:
            result = models.Result.objects.get(quiz=self.quiz)
            for answer in self.current_question.answer_set.all():
                obj = result.resultanswer_set.get(answer=answer)
                obj.employee_answer = False
                obj.save()
            result_answer = result.resultanswer_set.get(answer=answer_id)
            result_answer.employee_answer = True
            result_answer.save()


class QuizSummary:
    
    def _check_quiz(self):
        """prepares the data structure to the template"""
        score = 0
        max_points = 0
        result = models.Result.objects.get(quiz=self.quiz)
        questions = []
        for question in self.quiz.question_set.all():
            questions_dict = {}
            questions_dict['content'] = question.content
            max_points += question.points
            answers = []
            for answer in question.answer_set.all():
                answers_dict = {}
                answers_dict['content'] = answer.content
                is_correct = answer.is_correct
                employee_answer = answer.resultanswer_set.get(
                    result=result).employee_answer
                answers_dict['is_correct'] = is_correct
                answers_dict['employee_answer'] = employee_answer
                if is_correct and employee_answer:
                    score += question.points
                    questions_dict['result'] = True
                answers.append(answers_dict)
            questions_dict['answers'] = answers
            questions.append(questions_dict)
        self.max_points = max_points
        self.score = score
        self.questions = questions
        return questions

    def _prepare_summary(self, request):
        """function to prepare summary of test"""
        self.paginator = self.prepare_paginator(self._check_quiz)
        page = request.GET.get('page')
        questions = self.paginator.get_page(page)
        request.session['checking_question_number'] = page
        rate = round(self.score / self.max_points, 2)
        is_pass = False if rate < PASS_RATE else True
        context = {
            'score': self.score,
            'max_points': self.max_points,
            'status_quiz': self.quiz.is_active,
            'questions': questions,
            'rate': rate * 100,
            'is_pass': is_pass
        }
        return context
