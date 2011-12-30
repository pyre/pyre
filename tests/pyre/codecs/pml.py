#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


"""
Sanity check: verify that the package is accessible
"""


def test():
    import pyre.config

    # get the codec manager
    m = pyre.config.newCodecManager()
    # ask for a pml codec
    reader = m.newCodec(encoding="pml")
    # and return the manager and the reader
    return m, reader


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    test()


# end of file 
