
import pytest

from django.test import Client


@pytest.fixture
def client():
    """
    Client instance for testing
    :return : object
    :rtype: Client
    """
    client = Client()
    return client
