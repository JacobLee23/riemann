# riemann

![Repository Logo](docs/_static/riemann-logo.png)

**Riemann**, a pure-Python package for computing Riemann sums of functions of several real variables.

[![GitHub](https://img.shields.io/github/license/JacobLee23/riemann)](https://github.com/JacobLee23/riemann/blob/master/LICENSE)
![GitHub Pipenv locked Python version](https://img.shields.io/github/pipenv/locked/python-version/JacobLee23/riemann)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/riemann)](https://pypi.org/project/riemann)
[![GitHub tag (latest SemVer)](https://img.shields.io/github/v/tag/Jacoblee23/riemann)](https://github.com/JacobLee23/riemann/tags)

***

## Basic Usage

**Riemann** provides an intuitive syntax for calculating the Riemann sum of a function of several real variables over a closed multi-dimensional interval.

The below code snippet computes the Riemann sum of $f(x) = x^{2} + x$ over the interal $[0, 2]$ using 10 partitions using the left rule along the $x$-axis.

```python
>>> import riemann
>>> from riemann import Interval
>>> f = lambda x: x ** 2 + x
>>> intervals = [Interval(0, 2, 10)]
>>> rules = [riemann.Left]
>>> riemann.riemann_sum(f, intervals, rules)
Decimal('2.28')
```

However, **riemann** is not restricted to computing Riemann sums only over one dimension.
A similar syntax can be used to calculate the Riemann sum of a function of several real variables over a closed multi-dimensionl interval.
Additionally, different combinations of rules can be used to compute the Riemann sum.

See [Quickstart](https://riemann-py.readthedocs.io/en/latest/user/quickstart.html) for additional example usage of the **riemann** module.


## Features

- Fast computation of Riemann sums.
- Supports the computation of multi-dimensional Riemann sums.
- Supports the computation of the left, middle, and right Riemann sums.
- Supports the computation of the trapezoidal Riemann sum.
- Supports the computation of the upper and lower Darboux sums. (Under Development)

## Requirements

**Riemann** requires **Python 3.8+**. This project does not require any additional dependencies.

## Installation

```console
$ pip install riemann
```

## Documentation

[![Documentation Status](https://readthedocs.org/projects/riemann-py/badge/?version=latest)](https://riemann-py.readthedocs.io/en/latest/?badge=latest)

The documentation for this project is available on [Read the Docs](https://riemann-py.readthedocs.io/en/latest).
