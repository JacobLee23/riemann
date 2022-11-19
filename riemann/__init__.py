"""
.. :py:class:: Dim

    :canonical: riemann._summation.Dimension

.. :py:data:: L

    :canonical: riemann._summation.LOWER

.. :py:data:: M

    :canonical: riemann._summation.MIDDLE

.. :py:data:: U

    :canonical: riemann._summation.UPPER
"""

from .summation import LOWER, MIDDLE, UPPER
from .summation import Dimension
from .summation import rsum

# Type aliases
Dim = Dimension

# Global variable aliases
L, M, U = LOWER, MIDDLE, UPPER
