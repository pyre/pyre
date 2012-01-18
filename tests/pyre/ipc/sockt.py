#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


"""
Sanity check: verify that the socket factory is accessible
"""


def test():
    # get the package
    import pyre.ipc
    # make a socket
    return pyre.ipc.socket.open(address='ip4:localhost:22')


# main
if __name__ == "__main__":
    test()


# end of file 
