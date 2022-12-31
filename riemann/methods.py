"""
"""

from numbers import Number
import typing


def left(interval: typing.Tuple[Number, Number]) -> Number:
    """
    :param interval:
    :return:
    """
    return interval[0]


def middle(interval: typing.Tuple[Number, Number]) -> Number:
    """
    :param interval:
    :return:
    """
    return (interval[0] + interval[1]) / 2


def right(interval: typing.Tuple[Number, Number]) -> Number:
    """
    :param interval:
    :return:
    """
    return interval[1]
