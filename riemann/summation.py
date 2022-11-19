"""
.. py:class:: D

    :canonical: decimal.Decimal

.. py:class:: Number

    Type alias equivalent to

    .. code-block:: python

        typing.Union[int, float, decimal.Decimal]

.. py:data:: LOWER

    :type: int
    :value: 1

.. py:data:: MIDPOINT

    :type: int
    :value: 0

.. py:data:: UPPER

    :type: int
    :value: -1
"""

from decimal import Decimal
import itertools
import typing


# Type aliases
D = Decimal
Number = typing.Union[int, float, D]

LOWER, MIDPOINT, UPPER = -1, 0, 1


class Dimension(typing.NamedTuple):
    """
    .. :py:attribute:: a

        The lower bound of the rsum.

    .. :py:attribute:: b

        The upper bound of the rsum.

    .. :py:attribute:: n

        The number of partitions to divide the interval :math:`[a, b]`.

    .. :py:attribute:: method

        The Riemann rsum method to utilize. Should be equivalent to either :py:data:`LOWER`,
        :py:data:`MIDPOINT`, or :py:data:`UPPER`.
    """
    a: Number
    b: Number
    n: int
    method: int


def _displacements(
        bounds: tuple[D, D], dx: D, n: int, method: int
) -> typing.Generator[D, None, None]:
    """

    :param bounds:
    :param dx:
    :param n:
    :param method:
    :return:
    :raise ValueError:
    """
    if method == LOWER:
        return (bounds[0] + i * dx for i in range(0, n, 1))
    if method == MIDPOINT:
        return (bounds[0] + D(2 * i + 1) / 2 * dx for i in range(0, n, 1))
    if method == UPPER:
        return (bounds[0] + i * dx for i in range(1, n + 1, 1))
    raise ValueError


def rsum(func: typing.Callable, *args: Dimension):
    """

    :param func:
    :param args:
    :return:
    """
    values = []

    delta = D(1)

    for dim in args:
        a = D(str(dim.a) if isinstance(dim.a, float) else dim.a)
        b = D(str(dim.b) if isinstance(dim.b, float) else dim.b)
        dvar = (b - a) / dim.n

        values.append(list(_displacements((a, b), dvar, dim.n, dim.method)))
        delta *= dvar

    return delta * sum(func(*v) for v in itertools.product(*values))
