
from training.models import Answer, Question

QUESTIONS = ['Pierwsze', 'Drugie', 'Trzecie', 'Czwarte', 'Piąte', 'Szócte',
             'Siódme', 'Ósme', 'Dziewiąte', 'Dziesiąte', 'Jedenaste']

ANSWERS = ['pierwsza', 'druga', 'trzecia', 'czwarta', 'piąta', 'szósta']


def q_and_a():
    """function for filling relation question and related answer"""
    for question in QUESTIONS:
        q = Question.objects.create(content=f"{question} pytanie")
        for answer in ANSWERS:
            Answer.objects.create(
                question=q,
                content=f"{question} pytanie, {answer} odpowiedź"
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
        
        
