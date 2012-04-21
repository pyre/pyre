#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


"""
Exercise message ports
"""


def test():
    # access the package
    import mpi
    # get the world communicator
    world = mpi.world

    # check that the world has at least two tasks
    assert world.size > 1
    # get my rank
    rank = world.rank

    # if my rank is greater than 1
    if rank > 1: 
        # nothing for me to do
        return

    # establish a port between rank 0 and 1
    port = world.port(peer=(rank+1) % 2)

    # the root
    if rank == 0:
        # sends
        port.sendString("Hello {}!".format(port.peer))
    # the peer
    else:
        # receives
        message = port.recvString()
        # and checks
        assert message == "Hello {}!".format(rank)

    # repeat in reverse by sending the message as a pickled object
    # the peer
    if rank == 1:
        # sends
        port.send("Hello {}!".format(port.peer))
    # the root
    else:
        # receives
        message = port.recv()
        # and checks
        assert message == "Hello {}!".format(rank)
    
    # all done
    return


# main
if __name__ == "__main__":
    # import journal
    # journal.debug("mpi.ports").active = True
    test()


# end of file 
