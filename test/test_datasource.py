import pytest
import requests

from covid_bot.cogs.stats import API_GATEWAY, COUNTRY_SORT_KEYS
from covid_bot.utils.codes import COUNTRY_CODES_2


@pytest.fixture(scope="module")
def session():
    """ requests session for testing the API health """
    s = requests.Session()
    adapter = requests.adapters.HTTPAdapter(
        pool_connections=5, pool_maxsize=5, max_retries=10
    )
    s.mount("https://", adapter)
    s.mount("http://", adapter)

    yield s


def test_api_health(session):
    """ test site is up and the endpoints return 200 """
    resp = session.get(API_GATEWAY)
    assert resp.status_code == 200

    endpoints = ["timeline/global", "countries"]

    for ep in endpoints:
        resp = session.get(API_GATEWAY + "{}".format(ep))
        assert resp.status_code == 200


@pytest.mark.api
def test_country_sort_keys(session):
    """ test country keys are valid """
    query = API_GATEWAY + "countries/?sort="
    for key in COUNTRY_SORT_KEYS:
        print("Testing sort key = {}".format(key))
        resp = session.get(query + key)
        assert resp.status_code == 200


@pytest.mark.api
def test_country_codes(session):
    """ test to see if our country code list is valid """
    for k, v in COUNTRY_CODES_2.items():
        print("Testing country code {}:{}".format(k, v))
        resp = session.get(API_GATEWAY + "countries/{}".format(v))
        assert resp.status_code == 200
