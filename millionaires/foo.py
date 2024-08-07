


def count_to(n):
    until = n * (n + 1) // 2
    encountered = set()
    for c in range(1, 1 + until):
        for i in range(1, c+1):
            for j in range(1, i+1):
                if (i, j) not in encountered:
                    yield (i, j)
                encountered.add((i, j))


def naturals(until):
    yield from range(1, until + 1)


def integers(until):
    for v in naturals(until):
        yield v
        yield -v
    return


def rationals(until):
    for a in naturals(until):
        for b in naturals(a):
            yield (a, b)
            if a != b:
                yield (b, a)


from fractions import Fraction


def irationals(until):
    sent = set()
    for a in integers(until):
        for b in integers(a):
            if Fraction(a, b) in sent:
                continue
            yield (a, b)
            if abs(a) != abs(b):
                yield (b, a)
            sent.add(Fraction(a, b))
            sent.add(Fraction(b, a))
