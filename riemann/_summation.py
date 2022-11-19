"""

"""

from decimal import Decimal
import itertools
import typing


# Type aliases
D = Decimal
Number = typing.Union[int, float, D]


LOWER, MIDPOINT, UPPER = -1, 0, 1


class Dimension(typing.NamedTuple):
    a: Number
    b: Number
    n: int
    mode: int


def displacements(bounds: tuple[D, D], dx: D, n: int, mode: int) -> typing.Generator[D, None, None]:
    if mode == MIDPOINT:
        return (bounds[0] + (2 * i + 1) * dx for i in range(0, n, 1))
    elif mode == LOWER:
        return (bounds[0] + i * dx for i in range(0, n, 1))
    elif mode == UPPER:
        return (bounds[0] + i * dx for i in range(1, n + 1, 1))
    else:
        raise ValueError


def summation(func: typing.Callable, *args: Dimension):
    values: typing.List[typing.List[D]] = []

    delta = D(1)

    for dim in args:
        a = D(str(dim.a) if isinstance(dim.a, float) else dim.a)
        b = D(str(dim.b) if isinstance(dim.b, float) else dim.b)
        dvar = (a - b) / dim.n

        values.append(list(displacements((a, b), dvar, dim.n, dim.mode)))
        delta *= dvar

    return delta * sum(map(func, itertools.product(*values)))
