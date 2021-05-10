import pytest

from .conftest import client
from training.setup import QUESTIONS_IN_QUIZ

def test_input_no_user(client):
    resp = client.get("/question/")
    assert resp.status_code == 302
    assert resp.url == "/register/?next=/question/"


@pytest.mark.django_db
def test_input_with_user(client, django_user_model, setup_db):
    user = django_user_model.objects.create(username='501')
    client.force_login(user)
    client.post("/register/", {'username': '501'})
    resp = client.get("/question/")
    assert resp.status_code == 200
    

@pytest.mark.django_db
def test_content_page(client, django_user_model, setup_db):
    user = django_user_model.objects.create(username='501')
    client.force_login(user)
    client.post("/register/", {'username': '501'})
    resp = client.get("/question/")
    ctx = resp.context['questions']
    assert ctx.number == 1
    assert ctx.paginator.num_pages == QUESTIONS_IN_QUIZ
    assert 3 <= len(ctx[0]['answers']) <= 6
