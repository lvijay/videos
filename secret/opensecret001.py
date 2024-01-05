#!/usr/bin/env python3

from random import getrandbits
import turtle


def draw_human(t, radius=40, male=1):
    necklen = radius / 2
    bodylen = radius * 1.5
    limblen = radius
    t.circle(radius)
    p = t.pos()
    h = t.heading()
    if True:                    # draw arms
        t.setheading(h - 90)
        t.fd(necklen)
        t.setheading(h - 0)
        mypos = t.pos()
        t.fd(limblen)
        t.bk(2 * limblen)
        t.pu(); t.fd(limblen)
        t.setheading(h); t.setpos(*p); t.pd()
    if male:
        t.right(90)
        t.fd(bodylen)
        t.setheading(h - 30)
        t.fd(limblen); t.fd(-limblen)
        t.setheading(h + 180 + 30)
        t.fd(limblen)
    else:
        t.right(90)
        t.fd(necklen)
        t.begin_fill()
        t.right(90)
        t.circle(radius, steps=3)
        t.end_fill()
    t.pu()
    t.setheading(h)
    t.setpos(*p)
    t.pd()
    return mypos


def draw_conference(trtl, n, radius=270, headradius=30):
    extent = 360 / n
    positions = []
    for i in range(n):
        p = draw_human(trtl, radius=headradius, male=getrandbits(1))
        trtl.pu()
        trtl.circle(radius, extent)
        trtl.pd()
        positions.append(p)
    return positions


def main(tt):
    tt.degrees()
    tt.pu(); tt.sety(-200); tt.pd()
    tt.speed(10)
    return draw_conference(tt, 9)

    
if __name__ == '__main__':
    import turtle
    main(turtle)
    input()
    

#ordered = [lines[0]]
#while len(ordered) != 36:
#  cps, cpd = ordered[-1]
#  for pts, ptd in lines:
#    if cpd == pts and (pts, ptd) not in ordered:
#      ordered.append((pts, ptd))
#      break

## open-secret-001.py ends here
