
import pytest

from django.test import Client

from .utils import create_q_and_a, faker_employee


# @pytest.fixture
# def client():
#     """
#     Client instance for testing
#     :return : object
#     :rtype: Client
#     """
#     client = Client()
#     return client

@pytest.fixture
def setup_db():
    faker_employee()
    create_q_and_a()


@pytest.fixture
def logged_user(client, django_user_model):
    user = django_user_model.objects.create(username='555')
    client.force_login(user)
    return client


@pytest.fixture
def registered_user(logged_user, setup_db):
    # breakpoint()
    logged_user.post("/register/", {'username': '555'})
    return logged_user
