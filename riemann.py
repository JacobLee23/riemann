r"""
A pure-Python package for computing :math:`n`-dimensional Riemann sums.

-----

Let :math:`f: [a,b] \rightarrow \mathbb{R}` be a function defined on a closed interval
:math:`[a, b]` of the real numbers, :math:`\mathbb(R)`, and

.. math::

    P = ([x_{0}, x_{1}], [x_{1}, x_{2}], \dots , [x_{n-1}, x_{n}]),

a partition of :math:`[a, b]`, that is

.. math::

    a = x_{0} < x_{1} < x_{2} < \dots < x_{n} = b.

A Riemann sum of :math:`S` of :math:`f` over :math:`[a, b]` with partition :math:`P` is defined as

.. math::

    S = \sum_{i=1}^{n} f(x_{i}^{*}) \Delta x_{i},

where :math:`\Delta x_{i} = x_{i} - x_{i-1}` and :math:`x_{i}^{*} \in [x_{i-1}, x_{i}]`. One might
produce different Riemann sum depending on which :math:`x_{i}^{*}`'s are chosen.

Higher dimensional Riemann sums follow a similar pattern. An :math:`n`-dimensional Riemann sum is

.. math::

    S = \sum_{i=1}^{n} f(P_{i}^{*}) \Delta V_{i}

where :math:`P_{i}^{*} \in V_{i}`, that is, it is a point in the :math:`n`-dimensional cell
:math:`V_{i}` with :math:`n`-dimensional volume :math:`\Delta V_{i}`.

`Source <https://en.wikipedia.org/wiki/Riemann_sum>`_
"""

from decimal import Decimal
import functools
import inspect
import itertools
from numbers import Number
import operator
import typing


@typing.runtime_checkable
class FunctionSRV(typing.Protocol):
    r"""
    Callable type that represents a function of several real variables. Inherits from
    :class:`typing.Protocol`.

    .. math::

        f: \mathbb{R}^{n} \rightarrow \mathbb{R}

    Instances of this class are analagous to the following function:

    .. code-block:: python

        >>> def function(*x: Number) -> Number: ...

    The callable object takes any number of :class:`numbers.Number` objects and returns a single
    :class:`numbers.Number` object.

    This class uses the :func:`typing.runtime_checkable` decorator, so :func:`isinstance` can be
    to determine whether a callable object is an instance of this class:

    .. code-block:: python

        >>> from riemann import FunctionSRV
        >>> isinstance(lambda: 0, FunctionSRV)
        True
        >>> isinstance(lambda x: x, FunctionSRV)
        True
        >>> isinstance(lambda x, y: x * y, FunctionSRV)
        True
        >>> isinstance(lambda x, y, z: (x ** 2) * (y ** 2) * (z ** 2), FunctionSRV)
        True
    """
    def __call__(self, *args: Number) -> Number: ...


class RSumMethod:
    r"""
    .. math::

        \Delta x = \frac{b-a}{n}, i \in \{0, 1, \dots, n-1\}

    :param lower: The lower bound of the interval of summation
    :param length: The length of each partition of the interval of summation
    :return: The value of :math:`x_{i}^{*}`
    """
    def __call__(self, lower: Decimal, length: Decimal) -> Decimal:
        raise NotImplementedError


class Left(RSumMethod):
    r"""
    Specifies that the Left Riemann Sum method should be used over the corresponding dimension.
    Inherits from :py:class:`RSumMethod`.

    .. math::

        x_{i}^{*} = x_{i-1} = a + i \Delta x
    """
    def __call__(self, lower: Decimal, length: Decimal) -> Decimal:
        return lower


class Middle(RSumMethod):
    r"""
    Specifies that the Middle Riemann Sum method should be used over the corresponding dimension.
    Inherits from :py:class:`RSumMethod`.

    .. math::

        x_{i}^{*} = \frac{x_{i-1} + x_{i}}{2} = a + \frac{1}{2} i \Delta x
    """
    def __call__(self, lower: Decimal, length: Decimal) -> Decimal:
        return lower + length / 2


class Right(RSumMethod):
    r"""
    Specifies that the Right Riemann Sum method should be used over the corresponding dimension.
    Inherits from :py:class:`RSumMethod`.

    .. math::

        x_{i}^{*} = x_{i} = a + (i + 1) \Delta x
    """
    def __call__(self, lower: Decimal, length: Decimal) -> Decimal:
        return lower + length


LEFT, MIDDLE, RIGHT = Left(), Middle(), Right()


class Interval:
    """
    Represents the closed interval over which a Riemann sum is computed.

    :param lower: The lower bound of the interval
    :param upper: The upper bound of the interval
    :return: The number of partitions dividing the interval
    """
    def __init__(self, lower: Number, upper: Number, npartitions: int):
        self.lower = Decimal(str(lower) if isinstance(lower, float) else lower)
        self.upper = Decimal(str(upper) if isinstance(upper, float) else upper)
        self.npartitions = npartitions

        self.length = (self.upper - self.lower) / self.npartitions

    def __repr__(self):
        return "{}(lower={}, upper={}, npartitions={})".format(
            type(self).__name__,
            self.lower,
            self.upper,
            self.npartitions
        )

    def partitions(self, method: RSumMethod) -> typing.Generator[Decimal, None, None]:
        """
        :param method: The method to use for calculating the Riemann sum
        :return: A generator of the values of each partition of the interval
        """
        lower, length = self.lower, self.length

        for _ in range(self.npartitions):
            yield method(lower, length)

            lower += length


def riemann_sum(
    function: FunctionSRV, intervals: typing.Sequence[Interval], methods: typing.Sequence[RSumMethod]
):
    r"""
    Computes the Riemann Sum of a function of several variables over a closed multidimensional
    interval using indicated Riemann sum methods.

    The number of parameters of ``function``, the number of elements in ``intervals``, and the
    number of elements in ``methods`` all must be equal. In other words, every parameter in
    ``function`` must correspond to exactly one element in ``intervals`` and one element in
    ``methods``.

    .. note::

        The order of ``intervals`` and ``methods`` are significant.

        The first parameter of ``function`` corresponds to ``intervals[0]`` and ``methods[0]``, the
        second to ``intervals[1]`` and ``methods[1]``, the third to ``intervals[2]`` and
        ``methods[2]``, etc.

    :param function: A callable object representing function of several real variables
    :param intervals: The closed intervals over which the Riemann sum is calculated
    :param methods: The methods to use for calculating the Riemann sum
    :return: The value of the Riemann Sum over the indicated intervals using the indicated methods
    :raise ValueError: Length of the ``function`` parameter list, ``intervals``, and ``methods`` are unequal
    """
    ndimensions = len(inspect.signature(function).parameters)

    intervals = [x if isinstance(x, Interval) else Interval(*x) for x in intervals]
    if len(intervals) != ndimensions:
        raise ValueError(
            "The length of 'intervals' and the 'function' parameter list must be equal"
        )

    if len(methods) != ndimensions:
        raise ValueError(
            "The length of 'methods' and the 'function' parameter list must be equal"
        )

    delta = functools.reduce(operator.mul, (x.length for x in intervals))
    values = (x.partitions(m) for x, m in zip(intervals, methods))

    return (sum(function(*v) for v in itertools.product(*values)) * delta).normalize()


def trapezoidal_rule(
    function: FunctionSRV, intervals: typing.Sequence[Interval]
):
    r"""
    Computes the Riemann Sum of a function of several variables over a closed multidimensional
    interval using the trapezoidal rule.

    The number of parameters of ``function`` and the number of elements in ``intervals`` must be
    equal. In other words, every parameter in ``function`` must correspond to exactly one element
    in ``intervals``.

    .. note::

        The order of ``intervals`` is significant.

        The first parameter of ``function`` corresponds to ``intervals[0]``, the second to
        ``intervals[1]``, the third to ``intervals[2]``, etc.

    :param function: A callable object representing function of several real variables
    :param intervals: The closed intervals over which the Riemann sum is calculated
    :return: The value of the Riemann sum over the indicated intervals using the trapezoidal rule
    """
    methods = itertools.product((Left, Right), repeat=len(intervals))
    ncombinations = Decimal(2) ** len(intervals)

    return (sum(riemann_sum(function, intervals, m) for m in methods) / ncombinations).normalize()
