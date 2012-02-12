#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


"""
Instantiate a script
"""


def test():
    # access the package
    import pyre.shells
    # build a fork and return it
    return pyre.shells.fork(name="test")


# main
if __name__ == "__main__":
    test()


# end of file 
