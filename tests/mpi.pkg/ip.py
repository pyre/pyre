#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2023 all rights reserved
#


"""
Sanity check: show me the hostname of each machine in a communicator
"""


def test():
    # externals
    import mpi
    import socket

    # initialize mpi
    mpi.init()
    # get the world communicator
    world = mpi.world
    # get my ip address
    host = socket.gethostname()

    print("{0.rank:03}/{0.size:03}: {1}".format(world, host))

    # all done
    return


# main
if __name__ == "__main__":
    test()


# end of file
