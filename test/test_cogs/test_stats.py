import pytest
from unittest.mock import MagicMock

from covid_bot.cogs.stats import Stats, API_GATEWAY, discord

"""
Sunny day method tests

does not test:
    _plot_timeline
    async

"""


@pytest.fixture(scope="module")
def stats(mockbot, mocksession):
    """ stats cog mock for the module """
    mock_stats = MagicMock()
    mock_stats.bot = mockbot
    mock_stats._fetch_from_gateway.return_value = {
        "data": {
            "timeline": [
                {
                    "date": "date_val",
                    "cases": "cases_val",
                    "recovered": "recovered_val",
                    "deaths": "deaths_val",
                }
            ]
        }
    }
    mock_stats._get_countries_table.return_value = [
        {"country": "India", "other": ""},
        {"country": "France", "other": ""},
        {"country": "Germany", "other": ""},
    ]
    mock_stats._session = mocksession

    yield mock_stats


@pytest.fixture(scope="module", autouse=True)
def reset_stats_mock(stats):
    """ resets any side effects during a test """
    for i in stats.__dict__["_mock_children"].values():
        i.side_effect = None


def test_get_country_list(stats):
    assert Stats._get_country_list(stats) == ["India", "France", "Germany"]


def test_get_global_timeline(stats):
    Stats._get_global_timeline(stats)
    stats._fetch_from_gateway.assert_called_with("timeline", "global")


def test_get_country_timeline(stats):
    res = Stats._get_country_timeline(stats, "test_country")
    stats._fetch_from_gateway.assert_called_with("timeline", "test_country")
    assert res == {
        "date_val": {
            "cases": "cases_val",
            "recovered": "recovered_val",
            "deaths": "deaths_val",
        }
    }


def test_get_country_today(stats):
    assert Stats._get_country_today(stats, "France") == {
        "country": "France",
        "other": "",
    }


def test_get_top_countries(stats):
    res = Stats._get_top_countries(stats, "test_sort", n=2)
    stats._get_countries_table.assert_called_with(sorted_by="test_sort")
    assert res == [
        {"country": "India", "other": ""},
        {"country": "France", "other": ""},
    ]


def test_get_countries_table(stats):
    res = Stats._get_countries_table(stats)
    stats._fetch_from_gateway.assert_called_with("countries", sort="todayCases")
    assert res == {
        "data": {
            "timeline": [
                {
                    "date": "date_val",
                    "cases": "cases_val",
                    "recovered": "recovered_val",
                    "deaths": "deaths_val",
                }
            ]
        }
    }


def test_fetch_from_gateway(stats):
    ret = Stats._fetch_from_gateway(stats, "test_endpoint", "test_item")
    stats._session.get.assert_called_with(API_GATEWAY + "test_endpoint/test_item")
    assert ret == {"mock_content": "mock_content_val"}

    ret = Stats._fetch_from_gateway(
        stats, "test_endpoint", param1="val1", param2="val2"
    )
    stats._session.get.assert_called_with(
        API_GATEWAY + "test_endpoint?param1=val1,param2=val2"
    )
    assert ret == {"mock_content": "mock_content_val"}


def test_embed_response(stats, monkeypatch):
    embed_ret = MagicMock()
    EmbedMock = MagicMock(return_value=embed_ret)

    with monkeypatch.context() as m:
        m.setattr(discord, "Embed", EmbedMock)
        ret = Stats._embed_response(
            stats,
            description="test_descr",
            content=[{"name": "test_name", "value": "test_value"}],
        )

    EmbedMock.assert_called_with(description="test_descr", colour=discord.Colour.red())
    embed_ret.add_field.assert_called_with(name="test_name", value="test_value")
    assert ret == embed_ret


def test_response_template(stats):
    assert Stats._response_template(stats, "test") == {
        "description": "test",
        "content": [],
    }
