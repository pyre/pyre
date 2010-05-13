#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


"""
Sanity check: verify that the Ball shape behaves as expected
"""


def test():
    import gauss.shapes

    # instantiate
    ball = gauss.shapes.ball(name="ball")
    ball.radius = 1.0
    ball.center = [0.0, 0.0]

    # set up some interior points
    interior = [(0,0), (1,0), (0,1), (-1,0), (0,-1)]
    assert len(list(ball.contains(interior))) == len(interior)

    # set up some exterior points
    exterior = [(2,0), (0,2), (-2,0), (0,-2)]
    assert len(list(ball.contains(exterior))) == 0

    return ball


# main
if __name__ == "__main__":
    test()


# end of file 
