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

    .. py:attribute:: lower

        The lower bound of the interval.

        :type: :py:class:`decimal.Decimal`

    .. py:attribute:: upper

        The upper bound of the interval.

        :type: :py:class:`decimal.Decimal`
    """
    lower: Decimal
    upper: Decimal


@dataclass
class Method:
    """
    Abstract class for defining custom Riemann Sum methods. There is built-in support for the three
    most common Riemann Sum methods:

    - Left Riemann Sum method: :py:data:`riemann.LEFT`
    - Middle Riemann Sum method: :py:data:`riemann.MIDDLE`
    - Right Riemann Sum method: :py:data:`riemann.RIGHT`

    .. py:attribute:: name

        The name of the Riemann Sum method. This attribute is arbitrary and is solely used when
        representing a :py:class:`riemann.Method` object as a string (e.g., for debugging
        purposes).

        :type: str

    .. py:attribute:: func

        A callable object that takes three parameters:

        1. An :py:class:`riemann.Interval` object
        2. An ``int`` object
        3. A :py:class:`decimal.Decimal` object.

        Yields the value of the independent variable at the :math:`i`-th partition in the closed
        interval :math:`[a, b]`. 

        :type: typing.Callable
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
        Computes the values of the independent variable at each of the :math:`n` partitions in the
        closed interval :math:`[a, b]`.

        :param interval: The (closed) interval of the summation
        :param n: The number of partitions into which the interval of the summation is divided
        :param delta: The length of the each of the :math:`n` partition
        """
        return (self.func(interval, i, delta) for i in range(n))


LEFT = Method("left", lambda x, i, d: x.lower + i * d)
MIDDLE = Method("middle", lambda x, i, d: x.lower + Decimal(2 * i + 1) / 2 * d)
RIGHT = Method("right", lambda x, i, d: x.lower + (i + 1) * d)


@dataclass
class Dimension:
    """
    Contains the parameters of the summation over the dimension of interest.

    .. py:attribute:: a

        The lower bound of the interval of the summation.

        :type: numbers.Number

    .. py:attribute:: b

        The upper bound of the interval of the summation.

        :type: number.Number

    .. py:attribute:: n

        The number of partitions into which the interval of the summation :math:`[a, b]` is
        divided.

        :type: int

    .. py:attribute:: method

        The Riemann Sum method to use.

        :type: Method
    """
    a: Number
    b: Number
    n: int
    method: Method


def rsum(func: typing.Callable[..., Number], *args: Dimension):
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

    # Compute the :math:`n`-th dimensional Riemann Sum.
    return (delta * sum(func(*v) for v in itertools.product(*values))).normalize()
