from datetime import datetime
import json
import pytest
from src.utils import open_file, sort_list, clean_data, mask_requisites, format_operation, filter_func


@pytest.fixture
def filtered_sample_data():
    return [{'date': datetime(2018, 2, 3, 14, 52, 8, 93722),
             'description': 'Перевод с карты на карту',
             'from': 'MasterCard 4047671689373225',
             'id': 407169720,
             'operationAmount': {'amount': '67011.26',
                                 'currency': {'code': 'RUB', 'name': 'руб.'}},
             'state': 'EXECUTED',
             'to': 'Maestro 3806652527413662'},
            {'date': datetime(2019, 8, 26, 10, 50, 58, 294041),
             'description': 'Перевод организации',
             'from': 'Maestro 1596837868705199',
             'id': 441945886,
             'operationAmount': {'amount': '31957.58',
                                 'currency': {'code': 'RUB', 'name': 'руб.'}},             'state': 'EXECUTED',
             'to': 'Счет 64686473678894779589'},
            ]


@pytest.fixture
def unsorted_sample_data():
    return [{'date': datetime(2018, 2, 3, 14, 52, 8, 93722),
             'description': 'Перевод с карты на карту',
             'from': 'MasterCard 4047671689373225',
             'id': 407169720,
             'operationAmount': {'amount': '67011.26',
                                 'currency': {'code': 'RUB', 'name': 'руб.'}},
             'state': 'EXECUTED',
             'to': 'Maestro 3806652527413662'},
            {'date': datetime(2019, 8, 26, 10, 50, 58, 294041),
             'description': 'Перевод организации',
             'from': 'Maestro 1596837868705199',
             'id': 441945886,
             'operationAmount': {'amount': '31957.58',
                                 'currency': {'code': 'RUB', 'name': 'руб.'}},
             'state': 'EXECUTED',
             'to': 'Счет 64686473678894779589'},
            {'date': datetime(2019, 7, 3, 18, 35, 29, 512364),
             'description': 'Перевод организации',
             'from': 'MasterCard 7158300734726758',
             'id': 41428829,
             'operationAmount': {'amount': '8221.37',
                                 'currency': {'code': 'USD', 'name': 'USD'}},
             'state': 'CANCELED',
             'to': 'Счет 35383033474447895560'}]


@pytest.fixture
def sorted_sample_data():
    return [
        {'date': datetime(2019, 8, 26, 10, 50, 58, 294041),
         'description': 'Перевод организации',
         'from': 'Maestro 1596837868705199',
         'id': 441945886,
         'operationAmount': {'amount': '31957.58',
                             'currency': {'code': 'RUB', 'name': 'руб.'}},
         'state': 'EXECUTED',
         'to': 'Счет 64686473678894779589'},
        {'date': datetime(2019, 7, 3, 18, 35, 29, 512364),
         'description': 'Перевод организации',
         'from': 'MasterCard 7158300734726758',
         'id': 41428829,
         'operationAmount': {'amount': '8221.37',
                             'currency': {'code': 'USD', 'name': 'USD'}},
         'state': 'EXECUTED',
         'to': 'Счет 35383033474447895560'},
        {'date': datetime(2018, 2, 3, 14, 52, 8, 93722),
         'description': 'Перевод с карты на карту',
         'from': 'MasterCard 4047671689373225',
         'id': 407169720,
         'operationAmount': {'amount': '67011.26',
                             'currency': {'code': 'RUB', 'name': 'руб.'}},
         'state': 'EXECUTED',
         'to': 'Maestro 3806652527413662'}]


@pytest.fixture
def sample_data():
    return [{
        "id": 441945886,
        "state": "EXECUTED",
        "date": "2019-08-26T10:50:58.294041",
        "operationAmount": {
            "amount": "31957.58",
            "currency": {
                "name": "руб.",
                "code": "RUB"
            }
        },
        "description": "Перевод организации",
        "from": "Maestro 1596837868705199",
        "to": "Счет 64686473678894779589"
    },
        {
            "id": 41428829,
            "state": "EXECUTED",
            "date": "2019-07-03T18:35:29.512364",
            "operationAmount": {
                "amount": "8221.37",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод организации",
            "from": "MasterCard 7158300734726758",
            "to": "Счет 35383033474447895560"
        },
        {},
        {}]


@pytest.fixture
def cleaning_sample_data():
    return [{'date': datetime(2019, 8, 26, 10, 50, 58, 294041),
             'description': 'Перевод организации',
             'from': 'Maestro 1596837868705199',
             'id': 441945886,
             'operationAmount': {'amount': '31957.58',
                                 'currency': {'code': 'RUB', 'name': 'руб.'}},
             'state': 'EXECUTED',
             'to': 'Счет 64686473678894779589'},
            {'date': datetime(2019, 7, 3, 18, 35, 29, 512364),
             'description': 'Перевод организации',
             'from': 'MasterCard 7158300734726758',
             'id': 41428829,
             'operationAmount': {'amount': '8221.37',
                                 'currency': {'code': 'USD', 'name': 'USD'}},
             'state': 'EXECUTED',
             'to': 'Счет 35383033474447895560'}]


def test_open_file(sample_data, tmp_path):
    name = tmp_path / "test.json"
    with open(name, "w", encoding="utf-8") as file:
        json.dump(sample_data, file)
    assert open_file(name) == sample_data


def test_sort_list(cleaning_sample_data):
    assert sort_list(cleaning_sample_data) == cleaning_sample_data


def test_clean_data(sample_data, cleaning_sample_data):
    assert clean_data(sample_data) == cleaning_sample_data


def test_mask_requisites():
    data = "Maestro 4598300720424501"
    result = "Maestro 4598 30** **** 4501"
    assert mask_requisites(data) == result


def test_format_operation():
    data = {'date': datetime(2019, 8, 26, 10, 50, 58, 294041),
            'description': 'Перевод организации',
            'from': 'Maestro 1596837868705199',
            'id': 441945886,
            'operationAmount': {'amount': '31957.58',
                                'currency': {'code': 'RUB', 'name': 'руб.'}},
            'state': 'EXECUTED',
            'to': 'Счет 64686473678894779589'}

    assert format_operation(data) == ("26.08.2019 Перевод организации\n"
                                      "Maestro 1596 83** **** 5199 -> Счет **9589\n"
                                      "31957.58 руб.\n")


def test_filter_func(filtered_sample_data, unsorted_sample_data):
    assert filter_func(unsorted_sample_data) == filtered_sample_data

# def test_get_operations():
# data = open_file("../operations.json")
# cleaning_data = sort_list(clean_data(data))
# assert get_operations(count) == filter_func(cleaning_data)[:count]
