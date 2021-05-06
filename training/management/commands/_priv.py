
from django.contrib.auth import get_user_model
from django.utils import timezone
from faker import Faker
from random import randint

from training.models import Answer, Question, Quiz, Result

QUESTIONS = ['Pierwsze', 'Drugie', 'Trzecie', 'Czwarte', 'Piąte', 'Szóste',
             'Siódme', 'Ósme', 'Dziewiąte', 'Dziesiąte', 'Jedenaste']

ANSWERS = ['pierwsza', 'druga', 'trzecia', 'czwarta', 'piąta', 'szósta']

faker = Faker('pl_PL')
User = get_user_model()



def q_and_a():
    """function for filling relation question and related answer"""
    # for question in QUESTIONS:
    #     q = Question.objects.create(content=f"{question} pytanie")
    #     for answer in ANSWERS:
    #         Answer.objects.create(
    #             question=q,
    #             content=f"{question} pytanie, {answer} odpowiedź"
    #         )
    for question in range(77):
        q = Question.objects.create(
            content=f"Pytanie nr {question}: {faker.paragraph(nb_sentences=5)}"
        )
        for a in range(1, randint(3, 6)):
            Answer.objects.create(
                question=q,
                content=f"Odp nr {a}: {faker.paragraph(nb_sentences=3)}"
            )
    
        
def set_correct_answer():
    """
    function to set up one correct answer from
    answers related to the question
    """
    for obj in Question.objects.all():
        answer = obj.answer_set.all().order_by('?').first()
        answer.is_correct = True
        answer.save()
        

def create_users():
    for u in range(822, 833):
        User.objects.create(
            username=str(u),
            first_name=faker.first_name(),
            last_name=faker.last_name(), last_login = timezone.now()
        )

def generate_quiz(employee):
    questions = set()
    while len(questions) < 23:
        questions.add(Question.objects.all().order_by('?').first())
    quiz_object = Quiz.objects.create()
    result_object = Result.objects.create()
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
        
def quiz_for_users():
    for employee in User.objects.filter(username__contains='82'):
        generate_quiz(employee)
        