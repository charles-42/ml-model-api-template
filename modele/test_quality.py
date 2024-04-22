import pytest

def pytest_addoption(parser):
    parser.addoption("--myparam", action="store", default="default_value", help="My custom parameter")

@pytest.fixture
def myparam(request):
    return request.config.getoption("--myparam")
