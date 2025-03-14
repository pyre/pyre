#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2025 all rights reserved


"""
Sanity check: verify that the codec is accessible
"""


def test():
    # support
    import pyre.config

    # get the codec manager
    m = pyre.config.newConfigurator()
    # ask for a {yaml} codec
    reader = m.codec(encoding="yaml")
    # and return the manager and the reader
    return m, reader


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    test()


# end of file
