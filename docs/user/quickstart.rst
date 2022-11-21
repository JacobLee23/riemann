.. _quickstart:

Quickstart
==========

Below is a simple example for using the **Riemann** package.

Begin by importing the ``riemann`` package:

.. code-block:: python

    import riemann

Defining (Mathematical) Functions
---------------------------------

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

For each parameter taken by ``f``, a :py:class:`riemann.riemann.Dimension` object must be created,
which will contain the parameters for the summation of ``f`` over the corresponding dimension.

Since ``f`` takes only one parameter, only a single :py:class:`riemann.riemann.Dimension` object
needs to be created to contain the parameters for the summation of ``f`` over the :math:`x`
dimension.

For this example, ``f`` will be summed over the closed interval :math:`[0, 5]` using 10 partitions.
Furthermore, the left Riemann sum method (:py:data:`riemann.riemann.LOWER`) will be used.

.. code-block:: python

    >>> from riemann import Dimension
    >>> dim_x = Dimension(0, 5, 10, riemann.LEFT)
    >>> dim_x
    Dimension(a=0, b=5, n=10, method=Method('left'))

The other two Riemann sum methods with built-in support, the middle
(:py:data:`riemann.riemann.MIDDLE`) and right (:py:data:`riemann.riemann.RIGHT`) Riemann sum
methods, could also be used. Or, alternatively, a custom Riemann sum method can be defined and
used.

Defining Riemann Sum methods
----------------------------

There are three common Riemann sum methods, which all have built-in support:

- Left Riemann Sum: :py:data:`riemann.riemann.LOWER`
- Middle Riemann Sum: :py:data:`riemann.riemann.MIDDLE`
- Right Riemann Sum: :py:data:`riemann.riemann.RIGHT`

However, custom Riemann sum methods can be defined using the :py:class:`riemann.riemann.Method`
class. :py:class:`riemann.riemann.Method` is a ``dataclass`` (:py:func:`dataclasses.dataclass`)
that takes two parameters: (1) ``name``, a ``str`` object that is the name of the Riemann Sum
method; (2) ``func``, A callable object that takes three parameters (an
:py:class:`riemann.riemann.Interval` object, an ``int`` object, and a ``decimal.Decimal`` object)
and returns a generator of :py:class:`decimal.Decimal` objects. The ``name`` parameter is arbitrary
and is only used when representing a :py:class:`riemann.riemann.Method` object as a string. The
``func`` parameter yields the values of the independent variable at each of the :math:`n`
partitions in the closed interval :math:`[a, b]`.

For example, the left, middle, and right Riemann Sum methods are defined as follows:

.. code-block:: python

    from riemann import Method
    
    LEFT = Method("left", lambda x, i, d: x.lower + i * d)
    MIDDLE = Method("middle", lambda x, i, d: x.lower + Decimal(2 * i + 1) / 2 * d)
    RIGHT = Method("right", lambda x, i, d: x.lower + (i + 1) * d)

.. note::

    :py:meth:`riemann.riemann.Method.partitions` computes and yields the values of the independent
    variable at each of the partitions, not the values of the dependent variables. So Riemann Sum
    methods that rely on the value of the dependent variable at each of the partitions (e.g.,
    Trapezoidal Riemann Sum, Lower Riemann sum, Upper Riemann Sum) cannot be defined in this
    manner.

Computing Riemann Sums
----------------------

Once the function, dimension parameters, and (optional) Riemann Sum methods have been defined, the
Riemann sum itself can then be computed, using the :py:meth:`riemann.riemann.rsum` function. Simply
call the function, passing the callable object followed by the :math:`n`
:py:class:`riemann.riemann.Dimension` objects. The output is a single :py:class:`decimal.Decimal`
object.

.. code-block::

    >>> riemann.rsum(f, dim_x)
    Decimal('35.625')
