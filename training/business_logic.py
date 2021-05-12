
from training.setup import QUESTIONS_IN_QUIZ
from training import models


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
