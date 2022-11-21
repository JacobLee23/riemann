Riemann Documentation
======================

**Riemann** is a pure-Python package for computing the Riemann summation of functions in
:math:`n`-dimensional space.

-------------------------

**Riemann** provides an intuitive syntax for calculating the Riemann sum of a function over a
closed interval. The below code snippet computes the Riemann sum of :math:`f(x) = x^{2}` over the
interval :math:`[0, 2]` using 10 partitions along the :math:`x` axis.

.. doctest::
    :pyversion: > 3.7

    >>> import riemann
    >>> from riemann import Dimension
    >>> f = lambda x: x ** 2
    >>> dim_x = Dimension(0, 2, 10, riemann.LEFT)
    >>> dim_x
    Dimension(a=0, b=2, n=10, method=Method(name='lower'))
    >>> riemann.rsum(f, dim_x)
    Decimal('2.28')

However, **Riemann** is not restricted to computing Riemann sums only over one dimension. A similar
syntax can be used to calculate the Riemann sum of a function of several real variables over a
closed multi-dimensional interval. The below code snippet computes the Riemann sum of
:math:`f(x, y) = x^{2} y^{2}` over the interval :math:`x \in [0, 2], y \in [0, 4]` using 10
partitions along the :math:`x` axis and 10 partitions along the :math:`y` axis.

.. doctest::
    :pyversion: > 3.7

    >>> import riemann
    >>> from riemann import Dimension
    >>> f = lambda x, y: (x ** 2) * (y ** 2)
    >>> dim_x = Dimension(0, 2, 10, riemann.MIDDLE)
    >>> dim_x
    Dimension(a=0, b=2, n=10, method=Method(name='middle'))
    >>> dim_y = Dimension(0, 4, 10, riemann.MIDDLE)
    >>> dim_y
    Dimension(a=0, b=4, n=10, method=Method(name='middle'))
    >>> riemann.rsum(f, dim_x, dim_y)
    Decimal('56.6048')

The sole requirement is that the number of parameters taken by the function passed as the ``func``
argument to :py:func:`riemann.rsum` equals the number of :py:class:`riemann.Dimension` objects
passed.

Features
--------

- Fast computation of Riemann sum.
- Support for computation of multi-dimensional Riemann sum.
- Built-in support for left, middle, and right Riemann sum methods.
- Support for custom Riemann sum methods (using the :py:class:`riemann.Method` class).

User Guide
----------

.. toctree::
    :maxdepth: 2

    user/install
    user/quickstart

API Documentation
-----------------

.. toctree::

    api
