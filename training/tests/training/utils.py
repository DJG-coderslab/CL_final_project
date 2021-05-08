from django.contrib.auth import get_user_model
from faker import Faker

from training.management.commands._priv import q_and_a, set_correct_answer
from training.management.commands._groups import create_groups

User = get_user_model()
faker = Faker('pl_PL')


def faker_employee():
    User.objects.create(
        username='500',
        first_name=faker.first_name(),
        last_name=faker.last_name()
    )
    
def create_q_and_a():
    create_groups()
    q_and_a()
    set_correct_answer()
    
    