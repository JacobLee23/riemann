"""
"""

from dataclasses import dataclass
from decimal import Decimal
from numbers import Number
import typing


class Interval:
    """
    Contains the bounds of an interval.

    :param a: The lower bound of the interval
    :param b: The lower bound of the interval
    """
    def __init__(self, a: Number, b: Number):
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
    :param a: The lower bound of the interval
    :param b: The lower bound of the interval
    :param k: The number of subdivisions of the interval :math:`[a, b]`
    """
    def __init__(self, a: Number, b: Number, k: int):
        self._k = k

        super().__init__(a, b)

        self._length = (self.b - self.a) / self.k

    @property
    def k(self) -> int:
        """
        :return: The number of subdivisions of the interval :math:`[a, b]`
        """
        return self._k

    @property
    def length(self) -> Decimal:
        """
        :return: The length of each of the :math:`k` subdivisions of :py:attr:`interval`
        """
        return self._length

    def interval(self) -> Interval:
        """
        :return: A :py:class:`Interval` representing the object
        """
        return Interval(self.a, self.b)

    def subintervals(self) -> typing.Generator[Interval, None, None]:
        """
        """
        lower = self.a
        for _ in range(self.k):
            yield Interval(lower, lower + self.length)
            lower += self.length


@dataclass
class Method:
    """
    A class used for defining custom Riemann Sum methods. There is built-in support for the three
    most common Riemann Sum methods:

    - Left Riemann Sum method: :py:data:`riemann.LEFT`
    - Middle Riemann Sum method: :py:data:`riemann.MIDDLE`
    - Right Riemann Sum method: :py:data:`riemann.RIGHT`

    :param name: The name of the Riemann Sum method
    :param func: Returns the desired value bounded in an :py:class:`Interval` object
    """
    name: str
    func: typing.Callable[[Interval], Decimal]

    def __init__(self, name: str, func: typing.Callable[[Interval], Decimal]):
        self._name = name
        self._func = func

    @property
    def name(self) -> str:
        """
        This value is arbitrary and is solely used when representing a :py:class:`riemann.Method`
        objects as a string (i.e., for debugging purposes).

        :return: The name of the Riemann Sum method
        """
        return self._name

    @property
    def func(self) -> typing.Callable[[Interval], Decimal]:
        """
        A callable object that takes a :py:class:`Interval` object as its only parameters and
        returns a :class:`decimal.Decimal` representation of the desired value bounded in the
        interval.

        :return:
        """
        return self._func

    def __repr__(self) -> str:
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

    .. py:attribute:: a
    
        The lower bound of the interval

        :type: :class:`numbers.Number`
        
    .. py:attribute:: b
        
        The lower bound of the interval
        
    .. py:attribute:: k
        
        The number of subdivisions of the interval :math:`[a, b]`

    .. py:attribute:: method

        The Riemann Sum method to use.

        :type: :py:class:`Method`
    """
    a: Number
    b: Number
    k: int
    method: Method

    def interval(self) -> Interval:
        """
        :return:
        """
        return Interval(self.a, self.b)

    def subintervals(self) -> Subintervals:
        """
        :return:
        """
        return Subintervals(self.a, self.b, self.k)
