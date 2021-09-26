import time
import re


def date_valid(date):
    try:
        valid_date = time.strptime(date, '%Y-%m-%d')
        return True
    except ValueError:
        return False


def number_group_valid(number):
    try:
        num1, num2 = number.split("/")
        if len(num1) == 7 and len(num2) == 5:
            return True
        else:
            return False
    except ValueError:
        return False
