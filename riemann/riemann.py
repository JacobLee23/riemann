r"""
Computes the Riemann sum of functions in :math:`n`-dimensional space over a given interval.

.. py:data:: LOWER

    :type: int
    :value: 1

    Specifies that the function should use the Left Riemann Summation method.

    .. math::

        x_{i}^{*} = a+i\Delta x, \Delta x=\frac{b-a}{n}, i \in \{0,1,\dots,n-1\}

.. py:data:: MIDDLE

    :type: int
    :value: 0

    Specifices that the function should use the Middle Riemann Summation method.

    .. math::

        x_{i}^{*} = a+\frac{2i+1}{2}\Delta x, \Delta x=\frac{b-a}{n}, i \in \{0,1,\dots,n-1\}

.. py:data:: UPPER

    :type: int
    :value: -1

    Specifies that the function should use the Right Riemann Summation method.

    .. math::

        x_{i}^{*} = a+(i+1)\Delta x, \Delta x = \frac{b-a}{n}, i \in \{0,\dots,n-1\}
"""

from dataclasses import dataclass
from decimal import Decimal
import inspect
import itertools
from numbers import Number
import typing


@dataclass
class Interval:
    """
    Contains the bounds of an interval.

    .. :py:attribute:: lower

        The lower bound of the interval.

    .. :py:attribute:: upper

        The upper bound of the interval.
    """
    lower: Decimal
    upper: Decimal


@dataclass
class Method:
    """
    """
    name: str
    func: typing.Callable[[Interval, int, Decimal], Decimal]

    def __repr__(self) -> str:
        """
        """
        return f"Method(name='{self.name}')"

    def partitions(
        self, interval: Interval, n: int, delta: Decimal
    ) -> typing.Generator[Decimal, None, None]:
        """
        Computes the values of the independent variable at each of the partitions.

        :param interval: The closed interval of the summation
        :param n: The number of partitions into which the interval :math:`[a, b]` is divided
        :param delta: The length of the each partition in the interval
        """
        return (self.func(interval, i, delta) for i in range(n))


LOWER = Method("lower", lambda x, i, d: x.lower + i * d)
MIDDLE = Method("middle", lambda x, i, d: x.lower + Decimal(2 * i + 1) / 2 * d)
UPPER = Method("upper", lambda x, i, d: x.lower + (i + 1) * d)


class Dimension(typing.NamedTuple):
    """
    Contains the parameters of the summation on the dimension of interest.

    .. :py:attribute:: a

        The lower bound of the interval of summation.

    .. :py:attribute:: b

        The upper bound of the interval of summation.

    .. :py:attribute:: n

        The number of partitions into which the interval of summation :math:`[a, b]` is divided.

    .. :py:attribute:: method

        The Riemann sum method to use.
    """
    a: Number
    b: Number
    n: int
    method: Method


def rsum(func: typing.Callable[..., Number], *args: Dimension):
    r"""
    Computes the Riemann sum of functions in :math:`n`-dimensional space over a given interval.

    Parameter ``func`` can be written as :math:`f: {\mathbb{R}}^{n} \rightarrow \mathbb{R}`. The
    number of items in ``args`` must equal :math:`n`, the number of parameters of ``func`` and the
    number of dimensions of :math:`f`.

    :param func: A function of several real variables
    :param args:
    :return: The value of the Riemann sum for ``func``
    :raise ValueError: The number of dimensions does not equal the number of parameters of ``func``
    """
    if len(args) != len(inspect.signature(func).parameters):
        raise ValueError(
            "The number of values in 'args' does not equal the number of parameters of 'func'"
        )

    # Contains generators that yield the values to pass to the ``func``.
    # Each element represents one of the :math:`n` dimensions.
    values = []

    # :math:`\Delta V_{i}`
    delta = Decimal(1)

    # Iterate through the :math:`n` dimensions
    for dim in args:
        # Create :py:class:`Interval` object from bounds
        interval = Interval(
            Decimal(str(dim.a) if isinstance(dim.a, float) else dim.a),
            Decimal(str(dim.b) if isinstance(dim.b, float) else dim.b)
        )

        # Compute :math:`\Delta x` for the :math:`n`-th dimension.
        dvar = (interval.upper - interval.lower) / dim.n
        delta *= dvar

        values.append(dim.method.partitions(interval, dim.n, dvar))

    # Compute the :math:`n`-th dimensional Riemann sum.
    return (delta * sum(func(*v) for v in itertools.product(*values))).normalize()
