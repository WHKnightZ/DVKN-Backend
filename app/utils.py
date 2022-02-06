import datetime
import random
from marshmallow import fields, validate as validate_
from pytz import timezone

# from app.enums import CARD_RANK_PROBABILITIES


class FieldString(fields.String):
    """
    validate string field, max length = 1024
    Args:
        des:

    Returns:

    """
    DEFAULT_MAX_LENGTH = 1024  # 1 kB

    def __init__(self, validate=None, requirement=None, **metadata):
        """

        Args:
            validate:
            metadata:
        """
        if validate is None:
            validate = validate_.Length(max=self.DEFAULT_MAX_LENGTH)
        if requirement is not None:
            validate = validate_.NoneOf(error='Invalid input!', iterable={'full_name'})
        super(FieldString, self).__init__(validate=validate, required=requirement, **metadata)


class FieldNumber(fields.Number):
    """
    validate number field, max length = 30
    Args:
        des:

    Returns:

    """
    DEFAULT_MAX_LENGTH = 30  # 1 kB

    def __init__(self, validate=None, **metadata):
        """

        Args:
            validate:
            metadata:
        """
        if validate is None:
            validate = validate_.Length(max=self.DEFAULT_MAX_LENGTH)
        super(FieldNumber, self).__init__(validate=validate, **metadata)


def get_datetime_now() -> datetime:
    """
        Returns:
            current datetime
    """
    time_zon_sg = timezone('Asia/Ho_Chi_Minh')
    return datetime.datetime.now(time_zon_sg)


def get_timestamp_now() -> int:
    """
        Returns:
            current time in timestamp
    """
    time_zon_sg = timezone('Asia/Ho_Chi_Minh')
    return int(datetime.datetime.now(time_zon_sg).timestamp())


def get_timestamp_begin_today() -> int:
    """
        Returns:
            current time in timestamp
    """
    return get_timestamp_now() - get_timestamp_now() % 86400 - 7 * 3600


def is_contain_space(password: str) -> bool:
    """

    Args:
        password:

    Returns:
        True if password contain space
        False if password not contain space

    """
    return ' ' in password


def are_equal(arr1: list, arr2: list) -> bool:
    """
    Check two array are equal or not
    :param arr1: [int]
    :param arr2: [int]
    :return:
    """
    if len(arr1) != len(arr2):
        return False

    # Sort both arrays
    arr1.sort()
    arr2.sort()

    # Linearly compare elements
    for i, j in zip(arr1, arr2):
        if i != j:
            return False

    # If all elements were same.
    return True


def random_card(cards, probability_func):
    new_cards = [[card, 0] for card in cards]  # item[1] is probability
    sum_probability = 0

    for item in new_cards:
        probability = probability_func(item[0])
        sum_probability += probability
        item[1] = sum_probability

    rd = random.randint(0, sum_probability - 1)
    for item in new_cards:
        if rd <= item[1]:
            return item[0]


def random_card_register(cards):
    new_cards = [[card, 0] for card in cards]
    sum_probability = 0

    for item in new_cards:
        probability = item[0].probability_register
        sum_probability += probability
        item[1] = sum_probability

    arr = []
    for _ in range(5):
        rd = random.randint(0, sum_probability - 1)
        for item in new_cards:
            if rd <= item[1]:
                # rank = random_card(CARD_RANK_PROBABILITIES, lambda x: x["probability"])["rank"]
                rank = 0
                arr.append({"card": item[0], "rank": rank})
                break
    return arr
