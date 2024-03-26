import json
from datetime import datetime
from pprint import pprint


def open_file(name):
    """открываем файл и возвращаем список"""
    with open(name, "r", encoding="utf-8") as file:
        result = file.read()
        data = json.loads(result)
    return data


def sort_list(new_list):
    """сортируем список и оставляем последние 5 операций и отбрасываем ошибочные записи"""
    return sorted(new_list, key=lambda x: x['date'], reverse=True)


def clean_data(data):
    cleaning_data = []

    for i in data:
        try:
            i["date"] = datetime.fromisoformat(i["date"])
            cleaning_data.append(i)
        except KeyError:
            pass
    return cleaning_data


def mask_requisites(requisites):
    if requisites:
        if "Счет" in requisites:
            number = requisites.split()[-1]
            pref = "".join(requisites.split()[:-1])
            return f"{pref} **{number[-4:]}"
        else:
            number = requisites.split()[-1]
            pref = "".join(requisites.split()[:-1])
            return f"{pref} {number[:4]} {number[4:6]}** **** {number[12:]}"  # XXXX XX** **** XXXX
    else:
        return requisites


def format_operation(operation):
    """делаем операции читаемыми"""
    date = operation["date"].strftime("%d.%m.%Y")
    description = operation["description"]
    operation_from = mask_requisites(operation.get("from", ""))
    operation_to = mask_requisites(operation["to"])
    amount = operation['operationAmount']["amount"]
    currency = operation['operationAmount']["currency"]["name"]

    formatted_operation = (
        f"{date} {description}\n"
        f"{operation_from} -> {operation_to}\n"
        f"{amount} {currency}\n")

    return formatted_operation


def filter_func(data):
    return list(filter(lambda x: x["state"] == "EXECUTED", data))


def get_operations(count):
    data = open_file("../operations.json")
    cleaning_data = sort_list(clean_data(data))
    return filter_func(cleaning_data)[:count]
