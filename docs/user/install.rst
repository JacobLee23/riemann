.. _install:

Installation
============

**Riemann** required Python 3.7+.

Installing from PyPI
--------------------

Unix/macOS:

.. code-block:: console

    python3 -m pip install riemann


Windows:

.. code-block:: console

    py -m pip install riemann

Installing from GitHub
----------------------

**Riemann** is actively developed on GitHub: `Source Code <https://github.com/JacobLee23/riemann>`_.

First, clone the public repository:

.. code-block:: console

    git clone git://github.com/JacobLee23/riemann.git

After obtaining a copy of the source code, it can be embedded in a Python package. Or, it can be
installed into ``site-package``:

.. code-block:: console

    cd riemann
    python -m pip install .
