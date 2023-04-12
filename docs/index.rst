Riemann Documentation
======================

**Riemann**, a pure-Python package for computing :math:`n`-dimensional Riemann sums.

-------------------------

**Riemann** provides an intuitive syntax for calculating the Riemann sum of a function of several
real variables over a closed multi-dimensional interval.

Below is an example that computes the Riemann sum of the function :math:`f(x) = x^{2}` over the
closed interval :math:`[0, 1]` using 10 partitions along the :math:`x` axis.

.. doctest::
    :pyversion: > 3.8

    >>> import riemann
    >>> from riemann import Interval
    >>> f = lambda x: x ** 2
    >>> intervals = [Interval(0, 1, 10)]
    >>> methods = [riemann.Left]
    >>> riemann.riemann_sum(f, intervals, methods)
    Decimal('0.285')

Below is an example that computes the Riemann sum of the function :math:`f(x, y) = x^{2} + y^{2}`
over the the closed interal :math:`x \in [0, 1] y \in [0, 1]` using 10 partitions along the
:math:`x` axis and 10 partitions along the :math:`y` axis.

.. doctest::
    :pyversion: > 3.8

    >>> import riemann
    >>> from riemann import Interval
    >>> f = lambda x, y: x ** 2 + y ** 2
    >>> intervals = [Interval(0, 1, 10), Interval(0, 1, 10)]
    >>> methods = [riemann.Left, riemann.Left]
    >>> riemann.riemann_sum(f, intervals, methods)
    Decimal('0.57')

Below is an example that computes the Riemann sum of the function :math:`f(x, y) = x^{2} + y^{2}`
over the closed interval :math:`x \in [0, 1], y \in [0, 1], z \in [0, 1]` using 10 partitions
along the :math:`x` axis, 10 partitions along the :math:`y` axis, and 10 partitions along the
:math:`z` axis.

.. doctest::
    :pyversion: > 3.8

    >>> import riemann
    >>> from riemann import Interval
    >>> f = lambda x, y, z: x ** 2 + y ** 2 + z ** 2
    >>> intervals = [Interval(0, 1, 10), Interval(0, 1, 10), Interval(0, 1, 10)]
    >>> methods = [riemann.LEFT, riemann.LEFT, riemann.LEFT]
    >>> riemann.riemann_sum(f, intervals, methods)
    Decimal('0.855')

See :doc:`/user/quickstart` for more examples and more in-depth explanation.

Features
--------

- Fast computation of Riemann sums.
- Support for computation of multi-dimensional Riemann sums.
- Support for the left, middle, and right Riemann sum rules.
- Support for the trapezoidal Riemann sum rule.

User Guide
----------

.. toctree::
    :maxdepth: 2

    user/install
    user/quickstart

API Documentation
-----------------

.. toctree::
    :maxdepth: 1

    api
