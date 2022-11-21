.. _quickstart:

Quickstart
==========

Below is a simple example for using the **Riemann** package.

Begin by importing the ``riemann`` package:

.. code-block:: python

    import riemann

Defining a (Mathematical) Function
----------------------------------

First, define a function (or ``lambda``) to represent a mathematical function of several real
variables. The function can take any number of parameters (each of the arguments should be an
instance of :py:class:`numbers.Number`) and should evaluate to a single :py:class:`numbers.Number`
object.

For this example, the one-dimensional function :math:`f(x) = x^{2}` will be used:

.. code-block:: python

    >>> from numbers import Number
    >>> def f(x: Number) -> Number:
            return x ** 2

Similarly, using ``lambda`` syntax:

.. code-block:: python

    >>> f = lambda x: x ** 2

Defining Dimension Parameters
-----------------------------

For each parameter taken by ``f``, a :py:class:`riemann.Dimension` object must be created, which
will contain the parameters for the summation of ``f`` over the corresponding dimension.

Since ``f`` takes only one parameter, only a single :py:class:`riemann.Dimension` object needs to
be created to contain the parameters for the summation of ``f`` over the :math:`x` dimension.

For this example, :math:`f` will be summed over the closed interval :math:`[0, 5]` using 10
partitions. Furthermore, the left Riemann sum method (:py:data:`riemann..LOWER`) will be used.

.. code-block:: python

    >>> from riemann import Dimension
    >>> dim_x = Dimension(0, 5, 10, riemann.LEFT)
    >>> dim_x
    Dimension(a=0, b=5, n=10, method=Method('left'))

The other two Riemann sum methods with built-in support, the middle
(:py:data:`riemann.MIDDLE`) and right (:py:data:`riemann.RIGHT`) Riemann sum methods, could also be
used. Or, alternatively, a custom Riemann sum method can be defined and used.

Defining Riemann Sum Methods
----------------------------

There are three common Riemann sum methods, which all have built-in support:

- Left Riemann Sum: :py:data:`riemann.LOWER`
- Middle Riemann Sum: :py:data:`riemann.MIDDLE`
- Right Riemann Sum: :py:data:`riemann.RIGHT`

However, custom Riemann sum methods can be defined using the :py:class:`riemann.Method` class.
:py:class:`riemann.Method` is a ``dataclass`` (:py:func:`dataclasses.dataclass`) that takes two
parameters: :py:attr:`riemann.Method.name` and :py:attr:`riemann.Method.func`.

For example, the left, middle, and right Riemann Sum methods are defined as follows:

.. code-block:: python

    from riemann import Method
    
    LEFT = Method("left", lambda x, i, d: x.lower + i * d)
    MIDDLE = Method("middle", lambda x, i, d: x.lower + Decimal(2 * i + 1) / 2 * d)
    RIGHT = Method("right", lambda x, i, d: x.lower + (i + 1) * d)

.. note::

    :py:meth:`riemann.Method.partitions` computes and yields the values of the independent variable
    at each of the partitions, not the values of the dependent variables. So Riemann Sum methods
    that rely on the value of the dependent variable at each of the partitions (e.g., Trapezoidal
    Riemann Sum, Lower Riemann sum, Upper Riemann Sum) cannot be defined in this manner.

Computing the Riemann Sum
-------------------------

Once the function, dimension parameters, and (optional) Riemann Sum methods have been defined, the
Riemann sum itself can then be computed, using the :py:meth:`riemann.rsum` function. Simply call
the function, passing the callable object followed by the :math:`n` :py:class:`riemann.Dimension`
objects. The output is a single :py:class:`decimal.Decimal` object.

.. code-block::

    >>> riemann.rsum(f, dim_x)
    Decimal('35.625')

Generalization
--------------

The procedure for computing the Riemann Sum for a function of several real variables over an
arbitrary number of dimensions is quite similar to computing the Riemann Sum for a function of just
one variable over just one dimension.

As always, start by importing the **riemann** package:

.. code-block:: python

    >>> import riemann

1. **Defining a Mathematical Function**

Given the following function of :math:`n` real variables,

.. math::

    f: {\mathbb{R}}^{n} \rightarrow \mathbb{R},

the callable object ``f``, which takes :math:`n` arguments, can be defined as follows:

.. code-block:: python

    >>> f = lambda x1, x2, ..., xn: ...

2. **Defining Dimension Parameters**

The callable object ``f`` takes :math:`n` arguments, therefore :math:`n`
:py:class:`riemann.Dimension` must be created. In this generalization, :math:`f` will be summed
over the closed interval :math:`[a_{1}, b_{1}]` using :math:`k_{1}` partitions along the
:math:`x_{1}` axis, over the closed interval :math:`[a_{2}, b_{2}]` using :math:`k_{2}` partitions
along the :math:`x_{2}` axis, etc.

.. code-block:: python

    >>> from riemann import Dimension
    >>> dim_x1 = Dimension(a1, b1, k1, riemann.MIDDLE)
    >>> dim_x2 = Dimension(a2, b2, k2, riemann.MIDDLE)
    >>> ...
    >>> dim_xn = Dimension(an, bn, kn, riemann.MIDDLE)

3. **Computing the Riemann Sum**

Once the function and all :math:`n` :py:class:`riemann.Dimension` objects have been defined, the
:py:func:`riemann.rsum` function is called, passing the callable object of :math:`n` parameters
followed by the :math:`n` :py:class:`riemann.Dimension` objects. The result again is a single
:py:class:`decimal.Decimal` object.

.. code-block:: python

    >>> riemann.rsum(f, dim_x1, dim_x2, ..., dim_xn)
    Decimal(...)
