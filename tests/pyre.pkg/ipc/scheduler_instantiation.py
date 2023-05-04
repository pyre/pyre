#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2023 all rights reserved
#


"""
Sanity check: verify that schedulers can be instantiated
"""


def test():
    # access the package
    import pyre.ipc
    # instantiate a scheduler
    s = pyre.ipc.scheduler()
    # and return it
    return s


# main
if __name__ == "__main__":
    test()


# end of file
