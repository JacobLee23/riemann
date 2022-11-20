r"""
.. py:class:: D

    :canonical: decimal.Decimal

.. py:class:: Number

    Type alias equivalent to

    .. code-block:: python

        typing.Union[int, float, decimal.Decimal]

.. py:data:: LOWER

    :type: int
    :value: 1

    Given :math:`x_{i}^{*} \in [x_{i-1},x_{i}]`, use :math:`x_{i}^{*} = x_{i-1}`

    Specifies that the function should use the Left Riemann Summation method.

.. py:data:: MIDDLE

    :type: int
    :value: 0

    Given :math:`x_{i}^{*} \in [x_{i-1},x_{i}]`, use :math:`x_{i}^{*} = \frac{x_{i} + x_{i-1}}{2}`

    Specifices that the function should use the Middle Riemann Summation method.

.. py:data:: UPPER

    :type: int
    :value: -1

    Given :math:`x_{i}^{*} \in [x_{i-1},x_{i}]`, use :math:`x_{i}^{*} = x_{i}`

    Specifies that the function should use the Right Riemann Summation method.
"""

from decimal import Decimal
import inspect
import itertools
import typing


# Type aliases
Number = typing.Union[int, float, Decimal]

LOWER, MIDDLE, UPPER = -1, 0, 1


class Dimension(typing.NamedTuple):
    """
    Contains the conditions for computing a Riemann summation over a dimension.

    .. :py:attribute:: a

        The lower bound of the summation interval.

    .. :py:attribute:: b

        The upper bound of the summation interval.

    .. :py:attribute:: n

        The number of partitions into which the summation interval :math:`[a, b]` is divided.

    .. :py:attribute:: method

        The Riemann rsum method to utilize. Should be equivalent to either :py:data:`LOWER`,
        :py:data:`MIDDLE`, or :py:data:`UPPER`.
    """
    a: Number
    b: Number
    n: int
    method: int


def _partition_values(
        bounds: typing.Tuple[Decimal, Decimal], delta: Decimal, n: int, method: int
) -> typing.Generator[Decimal, None, None]:
    r"""
    Computes the values of the independent variable at the partitions of interest.

    Case 1: ``method = LOWER``

        .. math::

            x_{i}^{*} = a+i\Delta x, \Delta x=\frac{b-a}{n}, i \in \{0,1,\dots,n-1\}

    Case 2: ``method = MIDDLE``

        .. math::
            x_{i}^{*} = a+\frac{2i+1}{2}\Delta x, \Delta x=\frac{b-a}{n}, i \in \{0,1,\dots,n-1\}

    Case 3: ``method = UPPER``

        .. math::

            x_{i}^{*} = a+(i+1)\Delta x, \Delta x = \frac{b-a}{n}, i \in \{0,\dots,n-1\}

    :param bounds: A tuple of two values that represent the closed interval of the summation
    :param delta: The length of the each partition in the interval
    :param n: The number of partitions into which the interval :math:`[a, b]` is divided
    :param method: The identified of the Riemann summation method to use
    :return: The values of the independent variable at the partitions of interest
    :raise ValueError: An invalid Riemann summation method was used
    """
    # Iterate over the interval :math:`i \in ([0, n-1] \cap \mathbb{Z})`
    for i in range(0, n, 1):
        # Lower Riemann Summation method
        if method == LOWER:
            yield bounds[0] + i * delta
        # Middle Riemann Summation method
        elif method == MIDDLE:
            yield bounds[0] + Decimal(2 * i + 1) / 2 * delta
        # Upper Riemann Summation method
        elif method == UPPER:
            yield bounds[0] + (i + 1) * delta
        # Handle invalid Riemann Summation methods
        else:
            raise ValueError


def rsum(func: typing.Callable, *args: Dimension):
    r"""
    Computes the Riemann summation of functions in :math:`n`-dimensional space over a given
    interval.

    Parameter ``func`` can be written as :math:`f: {\mathbb{R}}^{n} \rightarrow \mathbb{R}`. The
    number of items in ``args`` must equal :math:`n`, the number of parameters of ``func`` and the
    number of dimensions of :math:`f`.

    :param func: A function of several real variables
    :param args:
    :return: The value of the Riemann summation for ``func``
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
        # Create :py:class:`decimal.Decimal` objects of numerical values
        a = Decimal(str(dim.a) if isinstance(dim.a, float) else dim.a)
        b = Decimal(str(dim.b) if isinstance(dim.b, float) else dim.b)

        # Compute :math:`\Delta x` for the :math:`n`-th dimension.
        dvar = (b - a) / dim.n
        delta *= dvar

        values.append(_partition_values((a, b), dvar, dim.n, dim.method))

    # Compute the :math:`n`-th dimensional Riemann summation.
    return delta * sum(func(*v) for v in itertools.product(*values))
