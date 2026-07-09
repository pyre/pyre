#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Sanity check: verify that the extension module is accessible
"""


def test():
    # access the extension module
    import mpi

    # initialize it
    ext = mpi.init()
    # get the world communicator
    world = ext.world()
    # extract the size of the communicator and my rank within it
    size = world.size
    rank = world.rank
    # verify that my rank is within range
    assert rank in range(size)

    # the communicator that holds me alone
    alone = ext.self()
    # has exactly one process
    assert alone.size == 1

    # asking again for the level of thread support reports what mpi settled on, as one of the
    # four levels it names
    assert isinstance(ext.initialize(), ext.Thread)

    # a reduction over whole numbers hands back a whole number
    assert isinstance(world.sum(item=rank), int)
    # and one over real numbers hands back a real number
    assert isinstance(world.sum(item=float(rank)), float)

    # all done
    return


# main
if __name__ == "__main__":
    test()


# end of file
