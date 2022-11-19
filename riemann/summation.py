r"""
Computes the Riemann summation of a function in :math:`n`-dimensional space.

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

where :math:`\Delta x_{i} = x_{i} - x{i-1}` and :math:`x_{i}^{*} \in [x_{i-1},x_{i}]`.

(`Source <https://en.wikipedia.org/wiki/Riemann_sum#Definition>`_)

From Wikipedia:

Specific choices of :math:`x_{i}^{*}` gives us different types of Riemann sums:

- If :math:`x_{i}^{*} = x_{i-1}` for all :math:`i`, then :math:`S` is called a **left rule** or **left Riemann sum**.
- If :math:`x_{i}^{*} = x_{i}` for all :math:`i`, then :math:`S` is called a **right rule** or **right Riemann sum**.
- If :math:`x_{i}^{*} = \frac{x_{i} + x_{i-1}}{2}` for all :math:`i`, then :math:`S` is called the **midpoint rule** or **middle Riemann sum**.

(`Source <https://en.wikipedia.org/wiki/Riemann_sum#Some_specific_types_of_Riemann_sums>`_)

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
D = Decimal
Number = typing.Union[int, float, D]

LOWER, MIDDLE, UPPER = -1, 0, 1


class Dimension(typing.NamedTuple):
    """
    .. :py:attribute:: a

        The lower bound of the summation.

    .. :py:attribute:: b

        The upper bound of the summation.

    .. :py:attribute:: n

        The number of partitions into which the interval :math:`[a, b]` is divided.

    .. :py:attribute:: method

        The Riemann rsum method to utilize. Should be equivalent to either :py:data:`LOWER`,
        :py:data:`MIDDLE`, or :py:data:`UPPER`.
    """
    a: Number
    b: Number
    n: int
    method: int


def _displacements(
        bounds: tuple[D, D], delta: D, n: int, method: int
) -> typing.Generator[D, None, None]:
    r"""
    Case 1: ``method = LOWER``

        .. math::

            x_{i}^{*} = a+i\Delta x, \Delta x=\frac{b-a}{n}, i \in \{0,1,\dots,n-1\}

    Case 2: ``method = MIDDLE``

        .. math::
            x_{i}^{*} = a+\frac{2i+1}{2}\Delta x, \Delta x=\frac{b-a}{n}, i \in \{0,1,\dots,n-1\}

    Case 3: ``method = UPPER``

        .. math::

            x_{i}^{*} = a+i\Delta x, \Delta x = \frac{b-a}{n}, i \in \{1,\dots,n\}

    :param bounds: A tuple of two values that represent the closed interval of the summation
    :param delta: The length of the each partition in the interval
    :param n: The number of partitions into which the interval :math:`[a, b]` is divided.
    :param method: The identified of the Riemann summation method to use
    :return:
    :raise ValueError:
    """
    for i in range(0, n, 1):
        if method == LOWER:
            yield bounds[0] + i * delta
        elif method == MIDDLE:
            yield bounds[0] + D(2 * i + 1) / 2 * delta
        elif method == UPPER:
            yield bounds[0] + (i + 1) * delta
        else:
            raise ValueError


def rsum(func: typing.Callable, *args: Dimension):
    """

    :param func:
    :param args:
    :return:
    :raise ValueError: The number of dimensions does not equal the number of parameters of ``func``
    """
    if len(args) != len(inspect.signature(func).parameters):
        raise ValueError(
            "The number of values in 'args' does not equal the number of parameters of 'func'"
        )

    values = []

    delta = D(1)

    for dim in args:
        a = D(str(dim.a) if isinstance(dim.a, float) else dim.a)
        b = D(str(dim.b) if isinstance(dim.b, float) else dim.b)
        dvar = (b - a) / dim.n

        values.append(list(_displacements((a, b), dvar, dim.n, dim.method)))
        delta *= dvar

    return delta * sum(func(*v) for v in itertools.product(*values))
