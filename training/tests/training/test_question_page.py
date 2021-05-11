import pytest

# from .conftest import client
from training.setup import QUESTIONS_IN_QUIZ
from training.models import Quiz


def test_input_no_user(client):
    resp = client.get("/question/")
    assert resp.status_code == 302
    assert resp.url == "/register/?next=/question/"


@pytest.mark.django_db
def test_input_with_user(registered_user):
    client = registered_user
    resp = client.get("/question/")
    assert resp.status_code == 200
    

@pytest.mark.django_db
def test_content_page(registered_user):
    client = registered_user
    resp = client.get("/question/")
    ctx = resp.context['questions']
    assert ctx.number == 1
    assert ctx.paginator.num_pages == QUESTIONS_IN_QUIZ
    assert 3 <= len(ctx[0]['answers']) <= 6


@pytest.mark.django_db
def test_post_answer(registered_user):
    client = registered_user
    resp = client.get("/question/")
    ctx = resp.context['questions']
    q_id = ctx[0].id
    choice = ctx[0]['answers'][2]['id']
    start_page = ctx.number
    assert all()
    cookies = client.cookies
    resp_post = client.post("/question/", {
        'employee_choice': choice,
        'answer_button': 'odpowiedź'
    })
    assert resp_post.context['questions'].number == start_page + 1
