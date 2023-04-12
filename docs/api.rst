.. _api:

API Reference
=============

.. automodule:: riemann

Let :math:`f: [a, b] \rightarrow \mathbb{R}` be a function defined on the closed interval :math:`[a, b]` of the real numbers, :math:`\mathbb{R}` and

.. math::

    P = ([x_{0}, x_{1}], [x_{1}, x_{2}], \dots , [x_{n-1}, x_{n}]),

a partition of :math:`[a, b]`, that is

.. math::

    a = x_{0} < x_{1} < x_{2} < \dots < x_{n} = b.

A Riemann sum of :math:`S` of :math:`f` over :math:`[a, b]` with partition :math:`P` is defined as

.. math::

    S = \sum_{i=1}^{n} f(x_{i}^{*}) \Delta x_{i},

where :math:`\Delta x_{i} = x_{i} - x_{i-1}` and :math:`x_{i}{*} \in [x_{i-1}, x_{i}]`.
One might produce different Riemann sum depending on which :math:`x_{i}^{*}`'s are chosen.

Higher dimensional Riemann sums follow a similar pattern.
An :math:`n`-dimensional Riemann sum is

.. math::

    S = \sum_{i=1}^{n} f(P_{i}^{*}) \Delta V_{i},

where :math:`P_{i}^{*} \in V_{i}`, that is, it is a point in the :math:`n`-dimensional cell :math:`V_{i}` with :math:`n`-dimensional volume :math:`\Delta V_{i}`.

`Source <https://en.wikipedia.org/wiki/Riemann_sum>`_

-----

.. autoclass:: FunctionSRV

.. autoclass:: RSumRule
    :members:

.. autoclass:: Left
    :members:

.. autoclass:: Middle
    :members:

.. autoclass:: Right
    :members:

.. autoclass:: Interval
    :members:

.. autofunction:: riemann_sum

.. autofunction:: trapezoidal_rule
