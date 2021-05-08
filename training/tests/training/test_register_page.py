import pytest

from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError

from training.models import Quiz, Question, Answer
from training.setup import QUESTIONS_IN_QUIZ

User = get_user_model()


@pytest.mark.django_db
def test_non_exists_user(client, setup_db):
    new_user = {
        'username': '555',
        'first_name': 'Ala',
        'last_name': 'Kozłowska'
    }
    resp = client.post('/register/', new_user)
    assert resp.status_code == 302
    user_from_db = User.objects.get(username='555')
    assert new_user['first_name'] == user_from_db.first_name
    assert Quiz.objects.filter(user=user_from_db).count() == 1
    assert Quiz.objects.filter(user=user_from_db).first().question_set.count() == QUESTIONS_IN_QUIZ
    assert Quiz.objects.filter(user=user_from_db).first().is_active is True
  
  
@pytest.mark.django_db
def test_exists_user(client, setup_db):
    user = User.objects.first()
    assert user.username == '500'
    assert user.quiz_set.count() == 0
    resp = client.post("/register/", {'username': '500'})
    assert resp.status_code == 302
    assert user.quiz_set.count() == 1
    assert user.quiz_set.first().is_active is True
  
   
@pytest.mark.django_db
def test_no_username(client, setup_db):
    user = {'first_name': 'Ala'}
    with pytest.raises(IntegrityError):
        resp = client.post("/register/", user)
