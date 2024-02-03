#/usr/bin/env python3

from random import random, shuffle


def divide(val: float, n):
    rands = [random() for _ in range(n)]
    total = sum(rands)
    dists = [r * val / total for r in rands]
    return dists


class Player:
    def __init__(self, name: str, salary: float, nplayers: int):
        self.__name = name
        self.__given: dict[Player, float] = {}
        self.__taken: dict[Player, float] = {}
        salary_random = divide(salary, nplayers)
        shuffle(salary_random)
        self.__divides = salary_random
    @property
    def name(self): return self.__name
    def exchange(self, asker: Player):
        if asker not in self.__given:
            given = self.__divides.pop()
        given = self.__given[asker]
        self.__taken[asker] = asker.exchange(self)
        return given
    def my_received_total(self): return sum(self.__taken.values())
    def __hash__(self): return hash(self.name)
    def __str__(self): return self.name
    def __repr__(self): return f'P<{str(self)}>'


if __name__ == '__main__':
    n = 9
    names = [f'p{i}' for i in range(n)]
    salaries = [(i+1)*1e6 for i in range(n)]
    players = [Player(f'{p}', s, n) for p,s in zip(names,salaries)]
    for pi in players:
        for pj in players:
            pi.exchange(pj)


## secret.py ends here
