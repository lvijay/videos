#!/usr/bin/env python

from random import SystemRandom

import simpleaudio


BEEP = simpleaudio.WaveObject.from_wave_file('./beep.wav')
BOOP = simpleaudio.WaveObject.from_wave_file('./boop.wav')

def play(b: bool):
    [BEEP, BOOP][b].play().wait_done()


if __name__ == "__main__":
    import sys

    r = SystemRandom()
    randbool = lambda: bool(r.randint(0, 1))
    soundlen = int(sys.argv[1])
    reps = int(sys.argv[2])
    data = [randbool() for i in range(soundlen)][::-1]
    res = data * reps
    print(''.join('^v'[v] for v in res))
    for v in res:
        play(v)


## is_it_random.py ends here
