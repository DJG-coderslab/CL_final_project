import pytest

from training.models import QuizDomain

@pytest.mark.django_db
def test_status_code(client):
    QuizDomain.objects.create(description='desc', manual='man')
    resp = client.get("/", {}, format='html')
    assert resp.status_code == 200
   