#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


"""
Exercise the spawning of daemons
"""


def test():
    import os
    # access the framework
    import pyre
    # instantiate a daemon and return it
    return pyre.shells.daemon(name="daemon")


# main
if __name__ == "__main__":
    test()


# end of file 
