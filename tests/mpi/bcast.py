#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


"""
Exercise broadcast operations
"""

class message:

    def __init__(self, data, **kwds):
        super().__init__(**kwds)
        self.data = data
        return

    def __eq__(self, other):
        return self.data == other.data


def test():
    # access the package
    import mpi
    # get the world communicator
    world = mpi.world
    # set up a root for the broadcast
    root = int(world.size / 2)
    # create a message
    item = message(data="Hello from {}".format(root))
    # broadcast it
    received = world.bcast(item=item, root=root)
    # check it
    assert received == item
    # all done
    return


# main
if __name__ == "__main__":
    test()


# end of file 
