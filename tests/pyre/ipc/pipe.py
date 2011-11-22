#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


"""
Sanity check: verify that the pipe factory is accessible
"""


def test():
    # get the package
    import pyre.ipc
    # make a pair of pipes
    return pyre.ipc.pipe.open()


# main
if __name__ == "__main__":
    test()


# end of file 
