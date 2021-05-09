import pytest

from .conftest import client

def test_input_no_user(client):
    resp = client.get("/question/")
    assert resp.status_code == 302
    assert resp.url == "/register/?next=/question/"

