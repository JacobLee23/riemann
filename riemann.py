r"""
Computes the Riemann Sum of functions of several variables over an arbitrary number of dimensions
over a given interval.

From Wikipedia:

    Let :math:`f: [a,b] \rightarrow \mathbb{R}` be a function defined on a closed interval
    :math:`[a,b]` of the real numbers, :math:`\mathbb(R)`, and

    .. math::

        P = \{[x_{0},x_{1}], [x_{1},x_{2}], \dots , [x_{n-1},x_{n}]\},

    be a partition of :math:`I`, where

    .. math::

        a = x_{0} < x_{1} < x_{2} < \dots < x_{n} = b.

    A Riemann sum of :math:`S` of :math:`f` over :math:`I` with partition :math:`P` is defined as

    .. math::

        S = \sum_{i=1}^{n} f(x_{i}^{*}) \Delta x_{i}

    where :math:`\Delta x_{i} = x_{i} - x_{i-1}` and :math:`x_{i}^{*} \in [x_{i-1},x_{i}]`.

(Source: `[1] <https://en.wikipedia.org/wiki/Riemann_sum#Definition>`_)

From Wikipedia:

    Higher dimensional Riemann sums follow a similar pattern as from one to two to three dimensions.
    For an arbitrary dimension, :math:`n`, a Riemann sum can be written as

    .. math::

        S = \sum_{i=1}^{n} f(P_{i}^{*}) \Delta V_{i}

    where :math:`P_{i}^{*} \in V_{i}`, that is, it's a point in the :math:`n`-dimensional cell
    :math:`V_{i}` with :math:`n`-dimensional volume :math:`\Delta V_{i}`.

(Source: `[2] <https://en.wikipedia.org/wiki/Riemann_sum#Arbitrary_number_of_dimensions>`_)
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
    """
    Callable type that represents a function of several real variables.
    """
    def __call__(self, *args: Number) -> Number: ...


class Method:
    """
    """


LEFT = type("Left", (Method,), {})()
MIDDLE = type("Middle", (Method,), {})()
RIGHT = type("Right", (Method,), {})()


class Interval:
    """
    Contains the bounds of an interval.

    :param a: The lower bound of the interval
    :param b: The upper bound of the interval
    :return: The number of subdivisions of the interval
    """
    def __init__(self, lower: Number, upper: Number, npartitions: int):
        self._lower = Decimal(str(lower) if isinstance(lower, float) else lower)
        self._upper = Decimal(str(upper) if isinstance(upper, float) else upper)
        self._npartitions = npartitions

        self._length = (self.upper - self.lower) / self.npartitions

    def __repr__(self):
        return "{}(lower={}, upper={}, npartitions={})".format(
            type(self).__name__,
            self.lower,
            self.upper,
            self.npartitions
        )

    @property
    def lower(self) -> Decimal:
        """
        :return: The lower bound of the interval
        """
        return self._lower

    @property
    def upper(self) -> Decimal:
        """
        :return: The upper bound of the interval
        """
        return self._upper

    @property
    def npartitions(self) -> int:
        """
        :return: The number of subdivisions of the interval
        """
        return self._npartitions

    @property
    def length(self) -> Decimal:
        """
        :return: The length of each of the :math:`k` subdivisions of the interval
        """
        return self._length

    def partitions(self, method: Method) -> typing.Generator[Decimal, None, None]:
        """
        Generates the values of the independent variable at each of the :py:attr:`k` partitions in
        the interval.

        :param method:
        :return:
        :raise ValueError: An unknown Riemann sum method was passed
        """
        lower, length = self.lower, self.length

        for _ in range(self.npartitions):
            if method is LEFT:
                yield lower
            elif method is MIDDLE:
                yield (2 * lower + length) / 2
            elif method is RIGHT:
                yield lower + length
            else:
                raise ValueError(
                    "Unknown Riemann sum method used"
                )

            lower += length


def normalize_summation(function: typing.Callable) -> typing.Callable:
    """
    """
    def wrapper(
        func: FunctionSRV, intervals: typing.Sequence[Interval], methods: typing.Sequence[Method]
    ):
        """
        """
        intervals = [x if isinstance(x, Interval) else Interval(*x) for x in intervals]

        if len(intervals) != len(inspect.signature(func).parameters):
            raise ValueError(
                "The length of 'intervals' does not equal the number of parameters of 'func'"
            )

        if len(methods) == 1:
            methods = [methods[0] for _ in inspect.signature(func).parameters]

        if len(methods) != len(inspect.signature(func).parameters):
            raise ValueError(
                "The length of 'args' must equal 1 or the number of parameters of 'func'"
            )

        return function(func, intervals, methods)

    return wrapper


@normalize_summation
def riemann_sum(
    func: FunctionSRV, intervals: typing.Sequence[Interval], methods: typing.Sequence[Method]
):
    r"""
    Computes the Riemann Sum of functions of several variables over an arbitrary number of
    dimensions over a given interval.

    Parameter ``func`` can be written as :math:`f: {\mathbb{R}}^{n} \rightarrow \mathbb{R}`. The
    number of items in ``args`` must equal :math:`n`, the number of parameters of ``func`` and the
    number of dimensions of :math:`f`.

    :param func: A function of several real variables
    :param intervals: The parameters of the summation over each of the dimensions
    :param methods:
    :return: The value of the Riemann Sum
    """
    delta = functools.reduce(operator.mul, (x.length for x in intervals))
    values = (x.partitions(m) for x, m in zip(intervals, methods))

    return (sum(func(*v) for v in itertools.product(*values)) * delta).normalize()


rsum = riemann_sum


def trapezoidal_rule(
    func: FunctionSRV, intervals: typing.Union[Interval, typing.Tuple[Number, Number, int]]
):
    r"""
    :param func: A function of several real variables
    :param intervals: The parameters of the summation over each of the dimensions
    :return:
    """
    methods = itertools.product((LEFT, RIGHT), repeat=len(intervals))
    ncombinations = Decimal(2) ** len(intervals)

    return (sum(riemann_sum(func, intervals, m) for m in methods) / ncombinations).normalize()


trule = trapezoidal_rule
