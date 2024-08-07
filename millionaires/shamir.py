#!/usr/bin/env python3


def eqn(n, k, secret, randgen):
    coefficients = [randgen() for _ in range(k - 1)] + [secret]
    return lambda x: sum([
        c * x**i
        for i, c in enumerate(reversed(coefficients))
    ])


## shamir.py ends here
