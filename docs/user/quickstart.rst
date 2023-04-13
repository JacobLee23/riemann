.. _quickstart:

Quickstart
==========

Computing Left, Middle, and Right Riemann Sums
----------------------------------------------

Compute left, middle, and right Riemann sums using the :py:func:`riemann.riemann_sum` function.

Generalization
^^^^^^^^^^^^^^

.. code-block:: python
    
    >>> from numbers import Number
    >>> import typing
    >>> import riemann
    >>> from riemann import Interval
    >>> def f(*x: Number) -> Number:
    ...     ...
    ...
    >>> intervals: typing.Sequence[riemann.Interval]
    >>> rules: typing.Sequence[riemann.RSumRule]
    >>> import riemann
    >>> from riemann import Interval
    >>> def f(*x: Decimal) -> Decimal: ...
    >>> intervals = [...]
    >>> rules = [...]
    >>> riemann.riemann_sum(f, intervals, rules)
    Decimal(...)

One Dimension
^^^^^^^^^^^^^

*Function*: :math:`f(x) = x^{2}`

+-----------+-------------------+---------------+---------------------------+
|           | Interval          | Partitions    | Rule                      |
+===========+===================+===============+===========================+
| :math:`x` | :math:`[0, 5]`    | 10            | :py:class:`riemann.Left`  |
+-----------+-------------------+---------------+---------------------------+

.. doctest::
    :pyversion: >= 3.8

    >>> import riemann
    >>> from riemann import Interval
    >>> f = lambda x: x ** 2
    >>> intervals = [Interval(0, 5, 10)]
    >>> rules = [riemann.Left]
    >>> riemann.riemann_sum(f, intervals, rules)
    Decimal('35.625')

Two Dimensions
^^^^^^^^^^^^^^

*Function*: :math:`f(x, y) = xy`

+-----------+-------------------+---------------+---------------------------+
|           | Interval          | Partitions    | Rule                      |
+===========+===================+===============+===========================+
| :math:`x` | :math:`[0, 5]`    | 10            | :py:class:`riemann.Right` |
+-----------+-------------------+---------------+---------------------------+
| :math:`y` | :math:`[0, 5]`    | 20            | :py:class:`riemann.Right` |
+-----------+-------------------+---------------+---------------------------+

.. doctest::
    :pyversion: >= 3.8

    >>> import riemann
    >>> from riemann import Interval
    >>> f = lambda x, y: x * y
    >>> intervals = [Interval(0, 5, 10), Interval(0, 5, 20)]
    >>> rules = [riemann.Right, riemann.Right]
    >>> riemann.riemann_sum(f, intervals, rules)
    Decimal('180.46875')

Three Dimensions
^^^^^^^^^^^^^^^^

*Function*: :math:`f(x, y, z) = x + y^{2} + z^{3}`

+-----------+-------------------+---------------+-------------------------------+
|           | Interval          | Partitions    | Rule                          |
+===========+===================+===============+===============================+
| :math:`x` | :math:`[0, 8]`    | 10            | :py:class:`riemann.Middle`    |
+-----------+-------------------+---------------+-------------------------------+
| :math:`y` | :math:`[0, 4]`    | 20            | :py:class:`riemann.Middle`    |
+-----------+-------------------+---------------+-------------------------------+
| :math:`z` | :math:`[0, 2]`    | 30            | :py:class:`riemann.Middle`    |
+-----------+-------------------+---------------+-------------------------------+

.. doctest::
    :pyversion: >= 3.8

    >>> import riemann
    >>> from riemann import Interval
    >>> f = lambda x, y, z: x + y ** 2 + z ** 3
    >>> intervals = [
    ...     Interval(0, 8, 10),
    ...     Interval(0, 4, 20),
    ...     Interval(0, 2, 30),
    ... ]
    >>> rules = [riemann.Middle, riemann.Middle, riemann.Middle]
    >>> riemann.riemann_sum(f, intervals, rules)
    Decimal('725.0488888888888888888888948')

Computing the Trapezoidal Riemann Sum
-------------------------------------

Compute trapezoidal Riemann sums using the :py:func:`riemann.trapezoidal_rule` function.

Generalization
^^^^^^^^^^^^^^

.. code-block:: python

    >>> from numbers import Number
    >>> import typing
    >>> import riemann
    >>> from riemann import Interval
    >>> def f(*x: Number) -> Number:
    ...     ...
    ...
    >>> intervals: typing.Sequence[riemann.Interval]
    >>> riemann.trapezoidal_rule(f, intervals)
    Decimal(...)

One Dimension
^^^^^^^^^^^^^

*Function*: :math:`f(x) = x^{2}`

+-----------+-------------------+---------------+
|           | Interval          | Partitions    |
+===========+===================+===============+
| :math:`x` | :math:`[0, 5]`    | 10            |
+-----------+-------------------+---------------+

.. doctest::
    :pyversion: >= 3.8

    >>> import riemann
    >>> from riemann import Interval
    >>> f = lambda x: x ** 2
    >>> intervals = [Interval(0, 5, 10)]
    >>> riemann.trapezoidal_rule(f, intervals)
    Decimal('41.875')

Two Dimensions
^^^^^^^^^^^^^^

*Function*: :math:`f(x, y) = xy`

+-----------+-------------------+---------------+
|           | Interval          | Partitions    |
+===========+===================+===============+
| :math:`x` | :math:`[0, 5]`    | 10            |
+-----------+-------------------+---------------+
| :math:`y` | :math:`[0, 5]`    | 20            |
+-----------+-------------------+---------------+

.. doctest::
    :pyversion: >= 3.8

    >>> import riemann
    >>> from riemann import Interval
    >>> f = lambda x, y: x * y
    >>> intervals = [Interval(0, 5, 10), Interval(0, 5, 20)]
    >>> riemann.trapezoidal_rule(f, intervals)
    Decimal('156.25')

Three Dimensions
^^^^^^^^^^^^^^^^

Three Dimensions
^^^^^^^^^^^^^^^^

*Function*: :math:`f(x, y, z) = x + y^{2} + z^{3}`

+-----------+-------------------+---------------+
|           | Interval          | Partitions    |
+===========+===================+===============+
| :math:`x` | :math:`[0, 8]`    | 10            |
+-----------+-------------------+---------------+
| :math:`y` | :math:`[0, 4]`    | 20            |
+-----------+-------------------+---------------+
| :math:`z` | :math:`[0, 2]`    | 30            |
+-----------+-------------------+---------------+

.. doctest::
    :pyversion: >= 3.8

    >>> import riemann
    >>> from riemann import Interval
    >>> f = lambda x, y, z: x + y ** 2 + z ** 3
    >>> intervals = [
    ...     Interval(0, 8, 10),
    ...     Interval(0, 4, 20),
    ...     Interval(0, 2, 30),
    ... ]
    >>> riemann.trapezoidal_rule(f, intervals)
    Decimal('725.9022222222222222222222276')

Computing the Upper and Lower Darboux Sums
------------------------------------------

.. note::

    Support for the computation of upper and lower Darboux sums is currently under development.

Compute upper and lower Darboux sums using the :py:func:`riemann.darboux_sum` function.

Two Dimensions
^^^^^^^^^^^^^^

*Function*: :math:`f(x, y) = xy`

+-----------+-------------------+---------------+---------------------------+
|           | Interval          | Partitions    | Rule                      |
+===========+===================+===============+===========================+
| :math:`x` | :math:`[0, 5]`    | 10            | :py:class:`riemann.Right` |
+-----------+-------------------+---------------+---------------------------+
| :math:`y` | :math:`[0, 5]`    | 20            | :py:class:`riemann.Right` |
+-----------+-------------------+---------------+---------------------------+

.. doctest::
    :pyversion: >= 3.8

    >>> import riemann
    >>> from riemann import Interval
    >>> f = lambda x, y: x * y
    >>> intervals = [Interval(0, 5, 10), Interval(0, 5, 20)]
    >>> rules = [riemann.Right, riemann.Right]
    >>> riemann.riemann_sum(f, intervals, rules)
    Decimal('180.46875')

Three Dimensions
^^^^^^^^^^^^^^^^

*Function*: :math:`f(x, y, z) = x + y^{2} + z^{3}`

+-----------+-------------------+---------------+-------------------------------+
|           | Interval          | Partitions    | Rule                          |
+===========+===================+===============+===============================+
| :math:`x` | :math:`[0, 8]`    | 10            | :py:class:`riemann.Middle`    |
+-----------+-------------------+---------------+-------------------------------+
| :math:`y` | :math:`[0, 4]`    | 20            | :py:class:`riemann.Middle`    |
+-----------+-------------------+---------------+-------------------------------+
| :math:`z` | :math:`[0, 2]`    | 30            | :py:class:`riemann.Middle`    |
+-----------+-------------------+---------------+-------------------------------+

.. doctest::
    :pyversion: >= 3.8

    >>> import riemann
    >>> from riemann import Interval
    >>> f = lambda x, y, z: x + y ** 2 + z ** 3
    >>> intervals = [
    ...     Interval(0, 8, 10),
    ...     Interval(0, 4, 20),
    ...     Interval(0, 2, 30),
    ... ]
    >>> rules = [riemann.Middle, riemann.Middle, riemann.Middle]
    >>> riemann.riemann_sum(f, intervals, rules)
    Decimal('725.0488888888888888888888948')

Computing the Trapezoidal Riemann Sum
-------------------------------------

Compute trapezoidal Riemann sums using the :py:func:`riemann.trapezoidal_rule` function.

Generalization
^^^^^^^^^^^^^^

.. code-block:: python

    >>> from numbers import Number
    >>> import typing
    >>> import riemann
    >>> from riemann import Interval
    >>> def f(*x: Number) -> Number:
    ...     ...
    ...
    >>> intervals: typing.Sequence[riemann.Interval]
    >>> rules: typing.Sequence[riemann.DSumRule]
    >>> riemann.darboux_sum(f, intervals, rules)
    Decimal(...)
