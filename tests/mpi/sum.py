#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


"""
Exercise sum reductions
"""


def test():
    # access the package
    import mpi
    # get the world communicator
    world = mpi.world
    # and its structure
    rank = world.rank
    size = world.size
    # set up a source for the reduction
    source = int(size / 2)
    # create a value
    number = rank**2
    # perform the reduction
    total = world.sum(item=number, source=source)
    # check it
    if rank == source:
        assert total == (size-1)*size*(2*size-1)/6
    # all done
    return


# main
if __name__ == "__main__":
    test()


# end of file 
