API Reference
=============

Installation
------------

To use the ``riemann`` package, first install it using ``pip``:

.. code-block:: console

    $ python -m pip install riemann


Basic Usage
-----------

>>> import riemann
>>> f = lambda x: x ** 2        # f(x) = x ** 2
>>> x_L = riemann.Dimension(0, 1, 4, riemann.L)     # Left Riemann Summation method
>>> x_M = riemann.Dimension(0, 1, 4, riemann.M)     # Middle Riemann Summation method
>>> x_R = riemann.Dimension(0, 1, 4, riemann.R)     # Right Riemann Summation method
>>> riemann.rsum(f, x_L)
Decimal('0.21875')
>>> riemann.rsum(f, x_M)
Decimal('0.328125')
>>> riemann.rsum(f, x_R)
Decimal('0.46875')
