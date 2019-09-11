import pytest

from client import RestfulOneQ


@pytest.fixture(scope="session")
def client():
    client = RestfulOneQ("https://one-q-api.test.net.biocad.ru")
    return client
