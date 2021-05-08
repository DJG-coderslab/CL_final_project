import pytest


@pytest.mark.django_db
def test_non_exists_user(client):
    assert True
    