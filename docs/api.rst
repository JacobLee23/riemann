API Reference
=============

Installation
------------

To use the ``riemann`` package, first install it using ``pip``:

.. code-block:: console

    $ python -m pip install riemann


Basic Usage
-----------

**Generalization** (:math:`n \in \mathbb{N}`): The below example computes a Riemann sum of a function of
:math:`n` real variables, using various permutations of the three Riemann sum methods:

.. math::

    f(x_{1}, x_{2}, \dots, x_{n}): {\mathbb{R}}^{n} \rightarrow \mathbb{R},
    x_{1} \in [a_{1}, b_{1}], x_{2} \in [a_{2}, b_{2}], \dots

.. doctest::
    :pyversion: > 3.6

    >>> import riemann      # doctest: +SKIP
    >>> from riemann import Dimension       # doctest: +SKIP

.. doctest::
    :pyversion: > 3.6

    >>> f = lambda x1, x2, ..., xn: ...     # doctest: +SKIP

The function ``f`` must have :math:`n` parameters.

.. doctest::
    :pyversion: > 3.6

    >>> varx1 = [Dimension(a1, b1, n1, riemann.L), Dimension(a1, b1, n1, riemann.M), Dimension(a1, b1, n1, riemann.U)]      # doctest: +SKIP
    >>> varx2 = [Dimension(a2, b2, n2, riemann.L), Dimension(a2, b2, n2, riemann.M), Dimension(a2, b2, n2, riemann.U)]      # doctest: +SKIP
    >>> ...     # doctest: +SKIP

.. doctest::
    :pyversion: > 3.6

    >>> riemann.rsum(f, varx1[0], varx2[0], ...)        # doctest: +SKIP
    >>> riemann.rsum(f, varx1[1], vary2[1], ...)        # doctest: +SKIP
    >>> riemann.rsum(f, varx1[2], vary2[2], ...)        # doctest: +SKIP
    >>> ... #doctest: +SKIP

Each call to :py:func:`riemann.summation.rsum` must contain :math:`n+1` elements (the function at position 0
followed by :math:`n` :py:class:`riemann.summation.Dimension` objects.

.. note::

    A total of :math:`3^{n} = 9` permutations of supported Riemann sum methods can be used for
    computing the ``n``-dimensional Riemann sum of a function of ``n`` real variables.


**1 Dimension** (:math:`n = 1`): The below example computes the Riemann sum of a function of 1 real
variable, using each of the three Riemann sum methods:

.. math::

    f(x) = x^{2}, x \in [0, 1], n_{x} = 4

.. doctest::
    :pyversion: > 3.6

    >>> import riemann
    >>> from riemann import Dimension
    >>> f = lambda x: x ** 2
    >>> varx = [Dimension(0, 1, 4, riemann.L), Dimension(0, 1, 4, riemann.M), Dimension(0, 1, 4, riemann.U)]
    >>> riemann.rsum(f, varx[0])
    Decimal('0.21875')
    >>> riemann.rsum(f, varx[1])
    Decimal('0.328125')
    >>> riemann.rsum(f, varx[2])
    Decimal('0.46875')

**2 Dimensions** (:math:`n = 2`): The below example computes a Riemann sum of a function of 2 real
variables, using various permutations of the three Riemann sum methods:

.. math::

    f(x,y) = xy, x \in [0, 1], y \in [0, 1], n_{x} = 4, n_{y} = 4

.. doctest::
    :pyversion: > 3.6

    >>> import riemann
    >>> from riemann import Dimension
    >>> f = lambda x, y: x * y
    >>> varx = [Dimension(0, 1, 4, riemann.L), Dimension(0, 1, 4, riemann.M), Dimension(0, 1, 4, riemann.U)]
    >>> vary = [Dimension(0, 1, 4, riemann.L), Dimension(0, 1, 4, riemann.M), Dimension(0, 1, 4, riemann.U)]
    >>> riemann.rsum(f, varx[0], vary[0])
    Decimal('0.140625')
    >>> riemann.rsum(f, varx[1], vary[1])
    Decimal('0.25')
    >>> riemann.rsum(f, varx[2], vary[2])
    Decimal('0.390625')
    >>> ...     # doctest: +SKIP

.. note::

    There are a total of :math:`3^{2} = 9` permutations of supported Riemann sum methods that can
    be used:

    +------+----------------+----------------+----------------+
    |      | y: L           | y: M           | y: U           |
    +------+----------------+----------------+----------------+
    | x: U | (x, y): (U, L) | (x, y): (U, M) | (x, y): (U, U) |
    +------+----------------+----------------+----------------+
    | x: M | (x, y): (M, L) | (x, y): (M, M) | (x, y): (M, U) |
    +------+----------------+----------------+----------------+
    | x: L | (x, y): (L, L) | (x, y): (L, M) | (x, y): (L, U) |
    +------+----------------+----------------+----------------+

    The above example only computes 3 of the 9 possible permutations.
