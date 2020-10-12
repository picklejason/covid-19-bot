import pytest
from unittest.mock import MagicMock


def pytest_addoption(parser):
    parser.addoption(
        "--api", action="store_true", help="runs the tests marked @pytest.mark.api"
    )


def pytest_runtest_setup(item):
    if "api" in item.keywords and not item.config.getoption("--api"):
        pytest.skip("API test.")


@pytest.fixture(scope="session")
def mockbot():
    """ bot mock for the pytest session """
    bot = MagicMock()
    yield bot


@pytest.fixture(scope="session")
def mocksession():
    """ requests session mock for pytest session """
    get_resp = MagicMock()
    get_resp.headers = {"Content-Type": "application/json"}
    get_resp.text = '{"mock_content":"mock_content_val"}'

    # probably a better way of mocking contexts, but this works well enough
    get = MagicMock()
    get.__enter__.return_value = get_resp

    session = MagicMock()
    session.get.return_value = get
    yield session
