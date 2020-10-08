"""Unit tests related to the api_client module."""
import pytest

import requests_mock
from cryptowatch.api_client import Client
from cryptowatch.exceptions import (CryptowatchAPIException,
                                    CryptowatchResponseException)

client = Client()


def test_get_assets(assets_keys, symbol=None):
    """Test an API call to get assets' info """
    response = client.get_assets(symbol)
    assert isinstance(response, dict)
    assert set(assets_keys).issubset(response.keys())


def test_get_assets_symbol(assets_keys, symbol='btc'):
    """Test an API call to get assets' info """
    response = client.get_assets(symbol)
    assert isinstance(response, dict)
    assert set(assets_keys).issubset(response.keys())
    assert symbol == response['result']['symbol']


def test_get_pairs(assets_keys, pair=None):
    """Test an API call to get pairs info """
    response = client.get_pairs(pair)
    assert isinstance(response, dict)
    assert set(assets_keys).issubset(response.keys())


def test_get_pairs_details(assets_keys, pair='btceur'):
    """Test an API call to get pair info """
    response = client.get_pairs(pair)
    assert isinstance(response, dict)
    assert set(assets_keys).issubset(response.keys())
    assert pair == response['result']['symbol']


def test_api_exception(symbol='invalid'):
    """Test API response Exception"""
    with pytest.raises(CryptowatchAPIException):
        client.get_assets(symbol)


def test_invalid_json(symbol='btc'):
    """Test Invalid response Exception"""

    with pytest.raises(CryptowatchResponseException):
        with requests_mock.mock() as m:
            m.get('https://api.cryptowat.ch/assets/btc', text='<head></html>')
            client.get_assets(symbol)


def test_get_markets(assets_keys):
    """Test an API call to get markets' info """
    response = client.get_markets()
    assert isinstance(response, dict)
    assert set(assets_keys).issubset(response.keys())


def test_get_single_exchange_market(assets_keys, exchange='gdax'):
    """Test an API call to get single exchange info """
    response = client.get_markets(exchange)
    assert isinstance(response, dict)
    assert set(assets_keys).issubset(response.keys())


def test_get_single_market(assets_keys):
    """Test an API call to get market detail """
    data = {
        'exchange': 'gdax',
        'pair': 'btcusd'
    }
    response = client.get_markets(data=data)
    assert isinstance(response, dict)
    assert set(assets_keys).issubset(response.keys())


def test_get_price(assets_keys):
    """Test an API call to get assets' info """
    data = {
        'exchange': 'gdax',
        'pair': 'btcusd',
        'route': 'price'
    }
    response = client.get_markets(data=data)
    assert isinstance(response, dict)
    assert set(assets_keys).issubset(response.keys())


@pytest.mark.parametrize('route', [
    'prices',
    'summaries',
])
def test_routes(assets_keys, route):
    """It returns a dict and contains expected keys"""
    response = client.get_aggregates(route)
    assert isinstance(response, dict)
    assert set(assets_keys).issubset(response.keys())


def test_get_agg_summaries_exception():
    """It raises ValueError with an incorrect argument."""
    with pytest.raises(ValueError):
        client.get_aggregates('test')


def test_get_agg_summaries_exception_no_arg():
    """It raises ValueError when no argument is passed."""
    with pytest.raises(ValueError):
        client.get_aggregates()
