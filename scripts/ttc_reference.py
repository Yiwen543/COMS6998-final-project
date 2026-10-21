"""Separate directed ceiling, never rendered to experimental model prompts."""
import random


def actions():
    def a(reset=0, write=0, read=0, addr=0, data=0):
        return dict(reset=reset, write=write, read=read, addr=addr, data=data)
    seq = [a(write=1, addr=2, data=1), a(write=1, addr=5, data=2),
           a(write=1, addr=3, data=7)]
    seq += [a(read=1, addr=i) for i in range(6)]
    seq += [a() for _ in range(18)]
    seq += [a(read=1, addr=0), a(read=1, addr=4), a(write=1, addr=4),
            a(read=1, addr=4), a(write=1, addr=3, data=0),
            a(read=1, addr=3), a(read=1, addr=15), a(write=1, addr=15, data=0xffffffff)]
    seq += [a(reset=1), a(write=1, addr=1, data=2), a(write=1, addr=2, data=0),
            a(write=1, addr=5, data=0), a(write=1, addr=3, data=5)]
    seq += [a() for _ in range(8)]
    seq += [a(read=1, addr=i) for i in (0, 1, 2, 3, 4, 5)]
    seq += [a(write=1, addr=4), a(read=1, addr=4)]
    rng = random.Random(6998)
    for i in range(96):
        choice = rng.randrange(7)
        if choice == 0:
            seq.append(a(write=1, addr=rng.choice((1, 2, 3, 5)), data=rng.getrandbits(32)))
        elif choice == 1:
            seq.append(a(read=1, addr=rng.randrange(16)))
        else:
            seq.append(a(data=rng.getrandbits(32)))
    seq += [a(read=1, addr=1), a(reset=1)]
    return seq
