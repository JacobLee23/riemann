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


Method = type("Method", (), {})
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
    def __init__(self, a: Number, b: Number, k: int):
        self._a = Decimal(str(a) if isinstance(a, float) else a)
        self._b = Decimal(str(a) if isinstance(b, float) else b)
        self._k = k

        self._length = (self.b - self.a) / self.k

    def __repr__(self):
        return "{}(a={}, b={}, k={})".format(
            type(self).__name__, self.a, self.b, self.k
        )

    @property
    def a(self) -> Decimal:
        """
        :return: The lower bound of the interval
        """
        return self._a

    lower = a

    @property
    def b(self) -> Decimal:
        """
        :return: The upper bound of the interval
        """
        return self._b

    upper = b

    @property
    def k(self) -> int:
        """
        :return: The number of subdivisions of the interval
        """
        return self._k

    partitions = k

    @property
    def length(self) -> Decimal:
        """
        :return: The length of each of the :math:`k` subdivisions of the interval
        """
        return self._length

    def subintervals(self, method: Method) -> typing.Generator[Decimal, None, None]:
        """
        :param method:
        :return:
        :raise ValueError:
        """
        x, dx = self.a, self.length

        for _ in range(self.k):
            if method is LEFT:
                yield x
            elif method is MIDDLE:
                yield (2 * x + dx) / 2
            elif method is RIGHT:
                yield x + dx
            else:
                raise ValueError(
                    "Unknown Riemann sum method used"
                )

            x += dx


def normalize_summation(f: typing.Callable) -> typing.Callable:
    """
    """
    def wrapper(
        func: typing.Callable[..., Number],
        intervals: typing.Sequence[Interval],
        methods: typing.Sequence[Method]
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

        return f(func, intervals, methods)

    return wrapper


@normalize_summation
def riemann_sum(
    func: typing.Callable[..., Number],
    intervals: typing.Sequence[Interval],
    methods: typing.Sequence[Method]
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
    values = (x.subintervals(m) for x, m in zip(intervals, methods))

    return (sum(func(*v) for v in itertools.product(*values)) * delta).normalize()


rsum = riemann_sum


def trapezoidal_rule(
    func: typing.Callable[..., Number],
    intervals: typing.Union[Interval, typing.Tuple[Number, Number, int]]
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
