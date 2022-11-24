"""
"""

from dataclasses import dataclass
from decimal import Decimal
from numbers import Number
import typing


class Interval:
    """
    Contains the bounds of an interval.
    """
    def __init__(self, a: Number, b: Number):
        """
        :param a: The lower bound of the interval
        :param b: The lower bound of the interval
        """
        self._a = Decimal(str(a) if isinstance(a, float) else a)
        self._b = Decimal(str(b) if isinstance(b, float) else b)

    @property
    def a(self) -> Decimal:
        """
        :return: The lower bound of the interval
        """
        return self._a

    @property
    def b(self) -> Decimal:
        """
        :return: The lower bound of the interval
        """
        return self._b

    @property
    def lower(self) -> Number:
        """
        Alias for :py:attr:`Interval.a`.
        """
        return self.a

    @property
    def upper(self) -> Number:
        """
        Alias for :py:attr:`Interval.b`.
        """
        return self.b


class Subintervals(Interval):
    """
    .. py:attribute:: a

        The lower bound of the interval.

        :type: :class:`numbers.Number`

    .. py:attribute:: b

        The upper bound of the interval.

        :type: :class:`numbers.Number`

    .. py:attribute:: k

        :type: int

    .. py:attribute:: interval

        :type: :py:class:`riemann.structures.Interval`
    """
    def __init__(self, a: Number, b: Number, k: int):
        """
        :param a: The lower bound of the interval
        :param b: The lower bound of the interval
        :param k: The number of subdivisions of the interval :math:`[a, b]`
        """
        self._k = k

        super().__init__(a, b)

    @property
    def k(self) -> int:
        """
        :return: The number of subdivisions of the interval :math:`[a, b]`
        """
        return self._k

    @property
    def interval(self) -> Interval:
        """
        :return:
        """
        return Interval(self.a, self.b)

    @property
    def length(self) -> Decimal:
        """
        :return: The length of each of the :math:`k` subdivisions of :py:attr:`interval`
        """
        return (self.b - self.a) / self.k

    def subintervals(self) -> typing.Generator[Interval, None, None]:
        """
        """
        return (
            Interval(
                self.a + i * self.length, self.a + (i + 1) * self.length,
            ) for i in range(self.k)
        )


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

        A callable object that takes a :py:class:`Interval` object as its only parameters and
        returns a :py:class:`decimal.Decimal` objects containing [TODO]

        :type: :class:typing.Callable:
    """
    name: str
    func: typing.Callable[[Interval], Decimal]

    def __repr__(self) -> str:
        """
        """
        return f"Method(name='{self.name}')"

    def partitions(self, subintervals: Subintervals) -> typing.Generator[Decimal, None, None]:
        """
        Computes the values of the independent variable at each of the :math:`n` partitions in the
        closed interval :math:`[a, b]`.

        :param subintervals:
        :return:
        """
        return map(self.func, subintervals.subintervals())


@dataclass
class Dimension:
    """
    Contains the parameters of the summation over the dimension of interest.

    .. py:attribute:: subintervals

        :type: :py:class:`Subintervals`

    .. py:attribute:: method

        The Riemann Sum method to use.

        :type: :py:class:`Method`
    """
    a: Number
    b: Number
    k: int
    method: Method

    @property
    def interval(self) -> Interval:
        """
        :return:
        """
        return Interval(self.a, self.b)

    @property
    def subintervals(self) -> Subintervals:
        """
        :return:
        """
        return Subintervals(self.a, self.b, self.k)
