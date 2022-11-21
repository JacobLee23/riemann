Riemann Documentation
======================

**Riemann** is a pure-Python package for computing the Riemann summation of functions in
:math:`n`-dimensional space.

-------------------------

.. doctest::
    :pyversion: > 3.6

    >>> import riemann
    >>> from riemann import Dimension
    >>> f = lambda x: x ** 2
    >>> var_x = Dimension(0, 2, 10, riemann.LOWER)
    >>> var_x.a
    0
    >>> var_x.b
    2
    >>> var_x.n
    10
    >>> var_x.method
    Method(name='lower')
    >>> riemann.rsum(f, var_x)
    Decimal('2.28')

However, **Riemann** is not restricted to computing Riemann sums only over one dimension.

.. doctest::
    :pyversion: > 3.6




Features
--------

User Guide
----------

.. toctree::

API Documentation
-----------------

.. toctree::

    api
