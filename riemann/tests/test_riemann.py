"""
Tests for :py:mod:`riemann.riemann`.
"""

from decimal import Decimal
import typing

import pytest

from riemann import riemann
from riemann.riemann import LEFT, MIDDLE, RIGHT
from riemann.riemann import Dimension
from riemann.riemann import rsum

F1D = [
    lambda x: 0,
    lambda x: 1,
    lambda x: x,
    lambda x: x ** 2,
    lambda x: x ** 3,
    lambda x: 1 / x,
    lambda x: 2 ** x,
]
F2D = [
    lambda x, y: 0,
    lambda x, y: 1,
    lambda x, y: x,
    lambda x, y: y,
    lambda x, y: x + y,
    lambda x, y: x * y, 
    lambda x, y: x ** 2 * y,
    lambda x, y: x * y ** 2,
    lambda x, y: x ** 2 + y ** 2,
    lambda x, y: x ** 2 * y ** 2,
]

@pytest.mark.parametrize(
    "func, dimensions, x", [
        (F1D[0], [Dimension(0, 1, 1, LEFT)], 0),
        (F1D[0], [Dimension(0, 1, 1, MIDDLE)], 0),
        (F1D[0], [Dimension(0, 1, 1, RIGHT)], 0),
        (F1D[0], [Dimension(-1, 0, 1, LEFT)], 0),
        (F1D[0], [Dimension(-1, 0, 1, MIDDLE)], 0),
        (F1D[0], [Dimension(-1, 0, 1, RIGHT)], 0),

        (F1D[1], [Dimension(0, 1, 1, LEFT)], 1),
        (F1D[1], [Dimension(0, 1, 1, MIDDLE)], 1),
        (F1D[1], [Dimension(0, 1, 1, RIGHT)], 1),
        (F1D[1], [Dimension(-1, 0, 1, LEFT)], 1),
        (F1D[1], [Dimension(-1, 0, 1, MIDDLE)], 1),
        (F1D[1], [Dimension(-1, 0, 1, RIGHT)], 1),

        (F1D[2], [Dimension(0, 1, 1, LEFT)], 0),
        (F1D[2], [Dimension(0, 1, 1, MIDDLE)], 1 / Decimal(2)),
        (F1D[2], [Dimension(0, 1, 1, RIGHT)], 1),
        (F1D[2], [Dimension(-1, 0, 1, LEFT)], -1),
        (F1D[2], [Dimension(-1, 0, 1, MIDDLE)], -1 / Decimal(2)),
        (F1D[2], [Dimension(-1, 0, 1, RIGHT)], 0),

        (F1D[3], [Dimension(0, 1, 1, LEFT)], 0),
        (F1D[3], [Dimension(0, 1, 1, MIDDLE)], 1 / Decimal(4)),
        (F1D[3], [Dimension(0, 1, 1, RIGHT)], 1),
        (F1D[3], [Dimension(-1, 0, 1, LEFT)], 1),
        (F1D[3], [Dimension(-1, 0, 1, MIDDLE)], 1 / Decimal(4)),
        (F1D[3], [Dimension(-1, 0, 1, RIGHT)], 0),
        (F1D[3], [Dimension(0, 2, 2, LEFT)], 1),
        (F1D[3], [Dimension(0, 2, 2, MIDDLE)], Decimal(5) / Decimal(2)),
        (F1D[3], [Dimension(0, 2, 2, RIGHT)], 5),
        (F1D[3], [Dimension(-2, 0, 2, LEFT)], 5),
        (F1D[3], [Dimension(-2, 0, 2, MIDDLE)], Decimal(5) / Decimal(2)),
        (F1D[3], [Dimension(-2, 0, 2, RIGHT)], 1),

        (F1D[4], [Dimension(0, 1, 1, LEFT)], 0),
        (F1D[4], [Dimension(0, 1, 1, MIDDLE)], 1 / Decimal(8)),
        (F1D[4], [Dimension(0, 1, 1, RIGHT)], 1),
        (F1D[4], [Dimension(-1, 0, 1, LEFT)], -1),
        (F1D[4], [Dimension(-1, 0, 1, MIDDLE)], -1 / Decimal(8)),
        (F1D[4], [Dimension(-1, 0, 1, RIGHT)], 0),
        (F1D[4], [Dimension(0, 2, 2, LEFT)], 1),
        (F1D[4], [Dimension(0, 2, 2, MIDDLE)], Decimal(7) / Decimal(2)),
        (F1D[4], [Dimension(0, 2, 2, RIGHT)], 9),
        (F1D[4], [Dimension(-2, 0, 2, LEFT)], -9),
        (F1D[4], [Dimension(-2, 0, 2, MIDDLE)], -Decimal(7) / Decimal(2)),
        (F1D[4], [Dimension(-2, 0, 2, RIGHT)], -1),

        (F1D[5], [Dimension(1, 2, 1, LEFT)], 1),
        (F1D[5], [Dimension(1, 2, 1, MIDDLE)], Decimal(2) / Decimal(3)),
        (F1D[5], [Dimension(1, 2, 1, RIGHT)], 1 / Decimal(2)),
        (F1D[5], [Dimension(-2, -1, 1, LEFT)], -1 / Decimal(2)),
        (F1D[5], [Dimension(-2, -1, 1, MIDDLE)], -Decimal(2) / Decimal(3)),
        (F1D[5], [Dimension(-2, -1, 1, RIGHT)], -1),
        (F1D[5], [Dimension(1, 3, 2, LEFT)], Decimal(3) / Decimal(2)),
        (F1D[5], [Dimension(1, 3, 2, MIDDLE)], Decimal(16) / Decimal(15)),
        (F1D[5], [Dimension(1, 3, 2, RIGHT)], Decimal(5) / Decimal(6)),
        (F1D[5], [Dimension(-3, -1, 2, LEFT)], -Decimal(5) / Decimal(6)),
        (F1D[5], [Dimension(-3, -1, 2, MIDDLE)], -Decimal(16) / Decimal(15)),
        (F1D[5], [Dimension(-3, -1, 2, RIGHT)], -Decimal(3) / Decimal(2)),

        (F1D[6], [Dimension(0, 1, 1, LEFT)], 1),
        (F1D[6], [Dimension(0, 1, 1, RIGHT)], 2),
        (F1D[6], [Dimension(-1, 0, 1, LEFT)], 1 / Decimal(2)),
        (F1D[6], [Dimension(-1, 0, 1, RIGHT)], 1),
        (F1D[6], [Dimension(0, 2, 2, LEFT)], 3),
        (F1D[6], [Dimension(0, 2, 2, RIGHT)], 6),
        (F1D[6], [Dimension(-2, 0, 2, LEFT)], Decimal(3) / Decimal(4)),
        (F1D[6], [Dimension(-2, 0, 2, RIGHT)], Decimal(3) / Decimal(2)),
    ]
)
def test_summation_1d(func: typing.Callable, dimensions: typing.Iterable[Dimension], x: Decimal):
    """

    :param func:
    :param dimensions:
    :param x:
    :return:
    """
    assert riemann.rsum(func, *dimensions) == x


@pytest.mark.parametrize(
    "func, dimensions, x", [
        (F2D[0], [Dimension(-1, 1, 2, LEFT), Dimension(-1, 1, 2, LEFT)], 0),
        (F2D[0], [Dimension(-1, 1, 2, MIDDLE), Dimension(-1, 1, 2, MIDDLE)], 0),
        (F2D[0], [Dimension(-1, 1, 2, RIGHT), Dimension(-1, 1, 2, RIGHT)], 0),

        (F2D[1], [Dimension(-1, 1, 2, LEFT), Dimension(-1, 1, 2, LEFT)], 4),
        (F2D[1], [Dimension(-1, 1, 2, MIDDLE), Dimension(-1, 1, 2, MIDDLE)], 4),
        (F2D[1], [Dimension(-1, 1, 2, RIGHT), Dimension(-1, 1, 2, RIGHT)], 4),

        (F2D[2], [Dimension(-1, 1, 2, LEFT), Dimension(-1, 1, 2, LEFT)], -2),
        (F2D[2], [Dimension(-1, 1, 2, MIDDLE), Dimension(-1, 1, 2, MIDDLE)], 0),
        (F2D[2], [Dimension(-1, 1, 2, RIGHT), Dimension(-1, 1, 2, RIGHT)], 2),

        (F2D[3], [Dimension(-1, 1, 2, LEFT), Dimension(-1, 1, 2, LEFT)], -2),
        (F2D[3], [Dimension(-1, 1, 2, MIDDLE), Dimension(-1, 1, 2, MIDDLE)], 0),
        (F2D[3], [Dimension(-1, 1, 2, RIGHT), Dimension(-1, 1, 2, RIGHT)], 2),

        (F2D[4], [Dimension(-1, 1, 2, LEFT), Dimension(-1, 1, 2, LEFT)], -4),
        (F2D[4], [Dimension(-1, 1, 2, MIDDLE), Dimension(-1, 1, 2, MIDDLE)], 0),
        (F2D[4], [Dimension(-1, 1, 2, RIGHT), Dimension(-1, 1, 2, RIGHT)], 4),

        (F2D[5], [Dimension(-1, 1, 2, LEFT), Dimension(-1, 1, 2, LEFT)], 1),
        (F2D[5], [Dimension(-1, 1, 2, MIDDLE), Dimension(-1, 1, 2, MIDDLE)], 0),
        (F2D[5], [Dimension(-1, 1, 2, RIGHT), Dimension(-1, 1, 2, RIGHT)], 1),

        (F2D[6], [Dimension(-1, 1, 2, LEFT), Dimension(-1, 1, 2, LEFT)], -1),
        (F2D[6], [Dimension(-1, 1, 2, MIDDLE), Dimension(-1, 1, 2, MIDDLE)], 0),
        (F2D[6], [Dimension(-1, 1, 2, RIGHT), Dimension(-1, 1, 2, RIGHT)], 1),

        (F2D[7], [Dimension(-1, 1, 2, LEFT), Dimension(-1, 1, 2, LEFT)], -1),
        (F2D[7], [Dimension(-1, 1, 2, MIDDLE), Dimension(-1, 1, 2, MIDDLE)], 0),
        (F2D[7], [Dimension(-1, 1, 2, RIGHT), Dimension(-1, 1, 2, RIGHT)], 1),

        (F2D[8], [Dimension(-1, 1, 2, LEFT), Dimension(-1, 1, 2, LEFT)], 4),
        (F2D[8], [Dimension(-1, 1, 2, MIDDLE), Dimension(-1, 1, 2, MIDDLE)], 2),
        (F2D[8], [Dimension(-1, 1, 2, RIGHT), Dimension(-1, 1, 2, RIGHT)], 4),

        (F2D[9], [Dimension(-1, 1, 2, LEFT), Dimension(-1, 1, 2, LEFT)], 1),
        (F2D[9], [Dimension(-1, 1, 2, MIDDLE), Dimension(-1, 1, 2, MIDDLE)], 1 / Decimal(4)),
        (F2D[9], [Dimension(-1, 1, 2, RIGHT), Dimension(-1, 1, 2, RIGHT)], 1),
    ]
)
def test_summation_2d(func: typing.Callable, dimensions: typing.Iterable[Dimension], x: Decimal):
    """

    :param func:
    :param dimensions:
    :param x:
    :return:
    """
    assert riemann.rsum(func, *dimensions) == x
