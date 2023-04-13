Riemann Documentation
======================

**Riemann**, a pure-Python package for computing :math:`n`-dimensional Riemann sums.

-------------------------

**Riemann** provides an intuitive syntax for calculating the Riemann sum of a function of several
real variables over a closed multi-dimensional interval.

The below code snippet computes the Riemann sum of :math:`f(x) = x^{2} + x` over the interal
:math:`[0, 2]` using 10 partitions using the left rule along the :math:`x`-axis.

.. doctest::
    :pyversion: >= 3.8

    >>> import riemann
    >>> from riemann import Interval
    >>> f = lambda x: x ** 2 + x
    >>> intervals = [Interval(0, 2, 10)]
    >>> rules = [riemann.Left]
    >>> riemann.riemann_sum(f, intervals, rules)
    Decimal('4.08')

However, **riemann** is not restricted to computing Riemann sums only over one dimension.
A similar syntax can be used to calculate the Riemann sum of a function of several real variables
over a closed multi-dimensionl interval.
Additionally, different combinations of rules can be used to compute the Riemann sum.

See :doc:`/user/quickstart` for additional example usage of the **riemann** module.

Features
--------

- Fast computation of Riemann sums.
- Supports the computation of multi-dimensional Riemann sums.
- Supports the computation of the left, middle, and right Riemann sums.
- Supports the computation of the trapezoidal Riemann sum.
- Supports the computation of the upper and lower Darboux sums. (Under Development)

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
