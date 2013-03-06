#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


"""
Exercise product reductions
"""


def test():
    # externals
    import mpi
    import math
    # get the world communicator
    world = mpi.world
    # and its structure
    rank = world.rank
    size = world.size
    # set up a source for the reduction
    source = int(size / 2)
    # create a value
    number = rank + 1
    # perform the reduction
    product = world.product(item=number, source=source)
    # check it
    if rank == source:
        assert product == math.factorial(size)
    # all done
    return


# main
if __name__ == "__main__":
    test()


# end of file 
