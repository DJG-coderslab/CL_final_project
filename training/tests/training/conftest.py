
import pytest

from django.test import Client

from .utils import create_q_and_a, faker_employee


@pytest.fixture
def client():
    """
    Client instance for testing
    :return : object
    :rtype: Client
    """
    client = Client()
    return client

@pytest.fixture
def setup_db():
    faker_employee()
    create_q_and_a()

