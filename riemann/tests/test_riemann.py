"""
Tests for :py:mod:`riemann.riemann`.
"""

from decimal import Decimal
import typing

import pytest

from riemann import riemann

# Type aliases
D = Decimal
Dim = riemann.Dimension

# Global variable aliases
L, M, U = riemann.LOWER, riemann.MIDDLE, riemann.UPPER


@pytest.mark.parametrize(
    "func, dimensions, x", [
        (lambda x: 0, [Dim(0, 1, 1, L)], 0),
        (lambda x: 0, [Dim(0, 1, 1, M)], 0),
        (lambda x: 0, [Dim(0, 1, 1, U)], 0),

        (lambda x: 1, [Dim(0, 1, 1, L)], 1),
        (lambda x: 1, [Dim(0, 1, 1, M)], 1),
        (lambda x: 1, [Dim(0, 1, 1, U)], 1),

        (lambda x: x, [Dim(0, 1, 1, L)], 0),
        (lambda x: x, [Dim(0, 1, 1, M)], 1 / D(2)),
        (lambda x: x, [Dim(0, 1, 1, U)], 1),

        (lambda x: x ** 2, [Dim(0, 1, 1, L)], 0),
        (lambda x: x ** 2, [Dim(0, 1, 1, M)], 1 / D(4)),
        (lambda x: x ** 2, [Dim(0, 1, 1, U)], 1),
        (lambda x: x ** 2, [Dim(0, 1, 2, L)], 1 / D(8)),
        (lambda x: x ** 2, [Dim(0, 1, 2, M)], D(5) / D(16)),
        (lambda x: x ** 2, [Dim(0, 1, 2, U)], D(5) / D(8)),
        (lambda x: x ** 2, [Dim(0, 2, 2, L)], 1),
        (lambda x: x ** 2, [Dim(0, 2, 2, M)], D(5) / D(2)),
        (lambda x: x ** 2, [Dim(0, 2, 2, U)], 5),
        (lambda x: x ** 2, [Dim(0, 2, 1, L)], 0),
        (lambda x: x ** 2, [Dim(0, 2, 1, M)], 2),
        (lambda x: x ** 2, [Dim(0, 2, 1, U)], 8),
        (lambda x: x ** 2, [Dim(1, 6, 10, L)], D(505) / D(8)),
        (lambda x: x ** 2, [Dim(1, 6, 10, M)], D(1145) / D(16)),
        (lambda x: x ** 2, [Dim(1, 6, 10, U)], D(645) / D(8)),
        (lambda x: x ** 2, [Dim(-10, 10, 50, L)], D(3336) / D(5)),
        (lambda x: x ** 2, [Dim(-10, 10, 50, M)], D(3332) / D(5)),
        (lambda x: x ** 2, [Dim(-10, 10, 50, U)], D(3336) / D(5)),

        (lambda x: x ** 3, [Dim(0, 1, 1, L)], 0),
        (lambda x: x ** 3, [Dim(0, 1, 1, M)], 1 / D(8)),
        (lambda x: x ** 3, [Dim(0, 1, 1, U)], 1),

        (lambda x: x ** 4 + x ** 2 - 4 * x + 3, [Dim(-5, 5, 25, L)], D(865578) / D(625)),
        (lambda x: x ** 4 + x ** 2 - 4 * x + 3, [Dim(-5, 5, 25, M)], D(847838) / D(625)),
        (lambda x: x ** 4 + x ** 2 - 4 * x + 3, [Dim(-5, 5, 25, U)], D(855578) / D(625)),
    ]
)
def test_summation_1d(func: typing.Callable, dimensions: typing.Iterable[Dim], x: D):
    """

    :param func:
    :param dimensions:
    :param x:
    :return:
    """
    assert riemann.rsum(func, *dimensions) == x


@pytest.mark.parametrize(
    "func, dimensions, x", []
)
def test_summation_2d(func: typing.Callable, dimensions: typing.Iterable[Dim], x: D):
    """

    :param func:
    :param dimensions:
    :param x:
    :return:
    """
    assert riemann.rsum(func, *dimensions) == x
