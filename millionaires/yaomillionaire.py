#!/usr/bin/env python3

from dataclasses import (
    InitVar,
    dataclass,
)
from math import (
    gcd,
    lcm,
)
from random import (
    choice,
)

from rsa.key import (
    calculate_keys_custom_exponent,
    find_p_q,
)



@dataclass
class RSA:
    p: int
    q: int
    n: int = None
    e: int = None
    d: int = None
    def __post_init__(self):
        self.n = self.p * self.q
        ctf = lcm(self.p - 1, self.q - 1) # carmichael's totient function
        e = choice([e for e in range(2, ctf) if gcd(e, ctf) == 1])
        e, d = calculate_keys_custom_exponent(self.p, self.q, e)
        self.e, self.d = min(e, d), max(e, d)
        return
    def encrypt(self, m: int):
        return pow(m, self.e, self.n)
    def decrypt(self, c: int):
        return pow(c, self.d, self.n)


def prime_pair(nbits):
    return find_p_q(nbits)




## yaomillionaire.py ends here
