#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2017 all rights reserved
#


"""
Sanity check: verify that the extension module is accessible
"""


def test():
    # access the extension module
    from mpi import mpi
    # get the world communicator
    world = mpi.world
    # extract the size of the communicator and my rank within it
    size = mpi.communicatorSize(world)
    rank = mpi.communicatorRank(world)
    # verify that my rank is within range
    assert rank in range(size)

    # for debugging purposes:
    # print("Hello from {}/{}!".format(rank, size))

    # all done
    return


# main
if __name__ == "__main__":
    test()


# end of file
