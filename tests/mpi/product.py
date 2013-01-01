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
    # set up a root for the reduction
    root = int(size / 2)
    # create a value
    number = rank + 1
    # perform the reduction
    product = world.product(item=number, root=root)
    # check it
    if rank == root:
        assert product == math.factorial(size)
    # all done
    return


# main
if __name__ == "__main__":
    test()


# end of file 
