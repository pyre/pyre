#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Exercise the spawning of daemons
"""


def test():
    # access the framework
    import pyre

    # instantiate a daemon and return it
    return pyre.shells.daemon()(name="daemon")


# main
if __name__ == "__main__":
    test()


# end of file
