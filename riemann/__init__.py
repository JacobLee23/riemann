"""
.. :py:class:: Dim

    :canonical: riemann._summation.Dimension

.. :py:data:: L

    :type: int
    :value: -1
    :canonical: riemann._summation.LOWER

.. :py:data:: M

    :type: int
    :value: 0
    :canonical: riemann._summation.MIDPOINT

.. :py:data:: U

    :type: int
    :value: 1
    :canonical: riemann._summation.UPPER
"""

from .summation import LOWER, MIDPOINT, UPPER
from .summation import Dimension
from .summation import rsum

# Type aliases
Dim = Dimension

# Global variable aliases
L, M, U = LOWER, MIDPOINT, UPPER
