.. _api:

API Reference
=============

.. automodule:: riemann

-----

.. autoclass:: Method
.. py:data:: LEFT

    Specifies that the Left Riemann Sum method should be used over the corresopnding dimension.

    .. math::

        x_{i}^{*} = a+i\Delta x, \Delta x=\frac{b-a}{n}, i \in \{0,1,\dots,n-1\}

    :type: Method

.. py:data:: MIDDLE

    Specifices that the Middle Riemann Sum method should be used over the corresponding dimension.

    .. math::

        x_{i}^{*} = a+\frac{2i+1}{2}\Delta x, \Delta x=\frac{b-a}{n}, i \in \{0,1,\dots,n-1\}

    :type: Method

.. py:data:: RIGHT

    Specifies that the Right Riemann Sum method should be used over the corresopnding dimension.

    .. math::

        x_{i}^{*} = a+(i+1)\Delta x, \Delta x = \frac{b-a}{n}, i \in \{0,\dots,n-1\}

    :type: Method

.. autoclass:: Interval
    :members:

.. autofunction:: riemann_sum
.. autofunction:: rsum

.. autofunction:: trapezoidal_rule
.. autofunction:: trule
