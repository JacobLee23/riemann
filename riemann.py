r"""
**Riemann**, a pure-Python package for computing :math:`n`-dimensional Riemann sums.
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
    Callable type that represents a function of several real variables.
    Inherits from :class:`typing.Protocol`.

    .. math::

        f: \mathbb{R}^{n} \rightarrow \mathbb{R}

    Instances of this class are analagous to the following function:

    .. code-block:: python

        >>> from numbers import Number
        >>> def function(*x: Number) -> Number: ...

    The callable object takes any number of :class:`numbers.Number` objects and returns a single
    :class:`numbers.Number` object.

    This class uses the :func:`typing.runtime_checkable` decorator, so :func:`isinstance` can be
    to determine whether a callable object is an instance of this class:

    .. doctest:: python

        >>> from numbers import Number
        >>> from riemann import FunctionSRV
        >>> def function(*x: Number) -> Number: ...
        >>> isinstance(function, FunctionSRV)
        True
        >>> def f():
        ...     return 0
        >>> isinstance(f, FunctionSRV)
        True
        >>> def g(x):
        ...     return x
        >>> isinstance(g, FunctionSRV)
        True
        >>> def h(x, y):
        ...     return x * y
        >>> isinstance(h, FunctionSRV)
        True
        >>> def i(x, y, z):
        ...     return x ** 2 + y ** 2 + z ** 2
        >>> isinstance(i, FunctionSRV)
        True
    """
    def __call__(self, *args: Number) -> Number: ...


class RSumRule:
    r"""
    Specifies that a particular Riemann sum rule should be used over an interval.
    """
    @classmethod
    def value(cls, lower: Decimal, length: Decimal) -> Decimal:
        r"""
        :param lower: The lower bound of the interval of summation
        :param length: The length of each partition of the interval of summation
        :return: The value of :math:`x_{i}^{*}`
        """
        raise NotImplementedError


class Left(RSumRule):
    r"""
    Specifies that the left rule should be used to compute the Riemann sum over an interval.
    """
    @classmethod
    def value(cls, lower: Decimal, length: Decimal) -> Decimal:
        r"""
        .. math::

            x_{i}^{*} = x_{i-1} = a + i \Delta x

        :param lower: The lower bound of the interval of summation
        :param length: The length of each partition of the interval of summation
        :return: The value of :math:`x_{i}^{*}`
        """
        return lower


class Middle(RSumRule):
    r"""
    Specifies that the midpoint rule should be used to compute the Riemann sum over an interval.
    """
    @classmethod
    def value(cls, lower: Decimal, length: Decimal) -> Decimal:
        r"""
        .. math::
        
            x_{i}^{*} = \frac{x_{i-1} + x_{i}}{2} = a + (i + \frac{1}{2}) \Delta x
            
        :param lower: The lower bound of the interval of summation
        :param length: The length of each partition of the interval of summation
        :return: The value of :math:`x_{i}^{*}`
        """
        return lower + length / 2


class Right(RSumRule):
    r"""
    Specifies that the right rule should be used to compute the Riemann sum over an interval.
    """
    @classmethod
    def value(cls, lower: Decimal, length: Decimal) -> Decimal:
        r"""
        .. math::
        
            x_{i}^{*} = x_{i} = a + (i + 1) \Delta x
            
        :param lower: The lower bound of the interval of summation
        :param length: The length of each partition of the interval of summation
        :return: The value of :math:`x_{i}^{*}`
        """
        return lower + length


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

    def partitions(self, rule: RSumRule) -> typing.Generator[Decimal, None, None]:
        """
        :param rule: The rule to use for compute the Riemann sum
        :return: A generator of the values of each partition of the interval
        """
        lower, length = self.lower, self.length

        for _ in range(self.npartitions):
            yield rule.value(lower, length)

            lower += length


def riemann_sum(
    function: FunctionSRV,
    intervals: typing.Sequence[Interval],
    rules: typing.Sequence[typing.Type[RSumRule]]
):
    r"""
    Computes the Riemann sum of a function of several variables over a closed multidimensional
    interval using specified Riemann sum rules.

    The following must all be equal:

    - The number of parameters of ``function``
    - The number of elements in ``intervals``
    - The number of elements in ``rules``.
    
    In other words, every parameter in ``function`` must correspond to exactly one element in
    ``intervals`` and one element in ``rules``.

    The order of ``intervals`` and ``rules`` is significant.
    During computation, each parameter of ``function`` is mapped to its corresponding element in
    ``intervals`` and its corresponding element in ``rules``.
    That is, the first parameter of ``function`` corresopnds to ``intervals[0]`` and ``rules[0]``,
    the second to ``intervals[1]`` and ``rules[1]``, etc.

    :param function: A callable object representing function of several real variables
    :param intervals: The closed intervals over which the Riemann sum is calculated
    :param rules: The rules to use for calculating the Riemann sum
    :return: The value of the Riemann sum over the indicated intervals using the indicated rules
    :raise ValueError: The ``function`` parameter list, ``intervals``, and ``rules`` are not equal in length
    """
    ndimensions = len(inspect.signature(function).parameters)

    if len(intervals) != ndimensions:
        raise ValueError(
            "The length of 'intervals' must equal the length of the parameter list of 'funcion'"
        )
    if len(rules) != ndimensions:
        raise ValueError(
            "The length of 'rules' must equal the length of the parameter list of 'function'"
        )

    delta = functools.reduce(operator.mul, (x.length for x in intervals))
    values = (x.partitions(r) for x, r in zip(intervals, rules))

    return (sum(function(*v) for v in itertools.product(*values)) * delta).normalize()


def trapezoidal_rule(
    function: FunctionSRV, intervals: typing.Sequence[Interval]
):
    r"""
    Computes the Riemann sum of a function of several variables over a closed multidimensional
    interval using the trapezoidal.

    This function utilizes the functionality of :py:func:`riemann_sum` to compute the Riemann sum.
    
    :param function: A callable object representing function of several real variables
    :param intervals: The closed intervals over which the Riemann sum is calculated
    :return: The value of the Riemann sum over the indicated intervals using the trapezoidal rule
    """
    rules = itertools.product((Left, Right), repeat=len(intervals))
    ncombinations = Decimal(2) ** len(intervals)

    return (sum(riemann_sum(function, intervals, r) for r in rules) / ncombinations).normalize()
