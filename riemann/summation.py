r"""
Contains the objects for computing the Riemann Sum of functions of several variables over an
arbitrary number of dimensions over a given interval.

.. py:data:: LEFT

    Specifies that the Left Riemann Sum method should be used over the corresopnding dimension.

    .. math::

        x_{i}^{*} = a+i\Delta x, \Delta x=\frac{b-a}{n}, i \in \{0,1,\dots,n-1\}

    :type: Method

.. py:data:: MIDDLE

    Specifices that the Middle Riemann Sum method should be used over the corresponding dimension.

    .. math::

        x_{i}^{*} = a+\frac{2i+1}{2}\Delta x, \Delta x=\frac{b-a}{n}, i \in \{0,1,\dots,n-1\}

    :type: Method

.. py:data:: RIGHT

    Specifies that the Right Riemann Sum method should be used over the corresopnding dimension.

    .. math::

        x_{i}^{*} = a+(i+1)\Delta x, \Delta x = \frac{b-a}{n}, i \in \{0,\dots,n-1\}

    :type: Method
"""

from decimal import Decimal
import functools
import inspect
import itertools
from numbers import Number
import typing

from .structures import Dimension
from .structures import Method
from .structures import Subintervals


LEFT = Method("left", lambda x: x.a)
MIDDLE = Method("middle", lambda x: (x.a + x.b) / 2)
RIGHT = Method("right", lambda x: x.b)


def check_dimensions(f: typing.Callable) -> typing.Callable:
    """
    """
    def wrapper(func: typing.Callable[..., Number], *args):
        """
        """
        if len(args) != len(inspect.signature(func).parameters):
            raise ValueError(
                "The number of values in 'args' does not equal the number of parameters of 'func'"
            )

        return f(func, *args)

    return wrapper


@check_dimensions
def riemann_sum(func: typing.Callable[..., Number], *args: Dimension):
    r"""
    Computes the Riemann Sum of functions of several variables over an arbitrary number of
    dimensions over a given interval.

    Parameter ``func`` can be written as :math:`f: {\mathbb{R}}^{n} \rightarrow \mathbb{R}`. The
    number of items in ``args`` must equal :math:`n`, the number of parameters of ``func`` and the
    number of dimensions of :math:`f`.

    :param func: A function of several real variables
    :param args: The parameters of the summation over each of the dimensions
    :return: The value of the Riemann Sum
    :raise ValueError: The number of dimensions does not equal the number of parameters of ``func``
    """
    # $\Delta V_{i}$
    delta = functools.reduce(lambda a, b: a * b, (d.subintervals.length for d in args))

    # Contains generators that yield the values to pass to the ``func``.
    # Each element represents one of the $n$ dimensions.
    values = (d.method.partitions(d.subintervals) for d in args)

    # Compute the $n$-th dimensional Riemann Sum.
    return (sum(func(*v) for v in itertools.product(*values)) * delta).normalize()


rsum = riemann_sum


@check_dimensions
def trapezoidal_rule(func: typing.Callable[..., Number], *args: Subintervals):
    r"""

    :param func:
    :param args:
    :return:
    :raise ValueError:
    """
    dimensions = itertools.product(
        *((Dimension(s.a, s.b, s.k, LEFT), Dimension(s.a, s.b, s.k, RIGHT)) for s in args)
    )

    return (sum(riemann_sum(func, *d) for d in dimensions) / Decimal(2) ** len(args)).normalize()


trule = trapezoidal_rule
