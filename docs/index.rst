Riemann Documentation
======================

**Riemann** is a pure-Python package for computing the Riemann summation of functions in
:math:`n`-dimensional space.

-------------------------

**Riemann** provides an intuitive syntax for calculating the Riemann sum of a function over a
closed interval. The below code snippet computes the Riemann sum of :math:`f(x) = x^{2}` over the
interval :math:`[0, 1]` using 10 partitions along the :math:`x` axis.

.. doctest::
    :pyversion: > 3.7

    >>> import riemann
    >>> from riemann import Interval
    >>> f = lambda x: x ** 2
    >>> var_x = Interval(0, 1, 10)
    >>> var_x
    Interval(a=0, b=1, k=10)
    >>> riemann.rsum(f, [var_x], [riemann.LEFT]) 
    Decimal('0.285')

However, **Riemann** is not restricted to computing Riemann sums only over one dimension. A similar
syntax can be used to calculate the Riemann sum of a function of several real variables over a
closed multi-dimensional interval. The below code snippet computes the Riemann sum of
:math:`f(x, y) = x^{2} + y^{2}` over the interval :math:`x \in [0, 1], y \in [0, 1]` using 10
partitions along the :math:`x` axis and 10 partitions along the :math:`y` axis.

.. doctest::
    :pyversion: > 3.7

    >>> import riemann
    >>> from riemann import Interval
    >>> f = lambda x, y: x ** 2 + y ** 2
    >>> var_x = Interval(0, 1, 10)
    >>> var_y = Interval(0, 1, 10)
    >>> var_x
    Interval(a=0, b=1, k=10)
    >>> var_y
    Interval(a=0, b=1, k=10)
    >>> riemann.rsum(f, [var_x, var_y], [riemann.LEFT, riemann.LEFT]) 
    Decimal('0.57')
    >>> riemann.rsum(f, [var_x, var_y], [riemann.LEFT])               
    Decimal('0.57')

The number of elements in the sequence passed as the second argument to :py:class:`riemann.rsum`
must equal the number of parameters taken by the function passed as the first argument to the
function. The number of elements in the sequence passed as the third argument to
:py:class:`riemann.rsum` must equal 1 or the number of parameters taken by the function passed as
the first argument to the function.

Features
--------

- Fast computation of Riemann sum.
- Support for computation of multi-dimensional Riemann sum.
- Built-in support for left, middle, and right Riemann sum methods.

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
