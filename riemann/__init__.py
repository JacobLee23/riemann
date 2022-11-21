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

from .riemann import LEFT, MIDDLE, RIGHT
from .riemann import Dimension
from .riemann import Interval
from .riemann import Method
from .riemann import rsum
