#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


"""
Exercise the group manipulation interface. This test assumes 4 or more processes
"""


def test():
    # access the package
    import mpi
    # grab the world communicator
    world = mpi.world
    # build a 4 process communicator out of world
    restricted = world.include(range(4))

    # if my rank is in [0,3]
    if world.rank in range(4):
        assert world.rank == restricted.rank
    else:
        assert restricted is None

    return


# main
if __name__ == "__main__":
    test()


# end of file 
