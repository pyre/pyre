#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


"""
Sanity check: verify that the package is accessible
"""


def test():
    import pyre.codecs

    # get the codec manager
    m = pyre.codecs.newManager()
    # ask for a pml codec
    reader = m.newCodec(encoding="pml")
    # open a stream
    sample = open("sample.pml")
    # read the contents
    inventory = reader.decode(sample)
    # check that we got a real instance back
    assert inventory is not None
    assert isinstance(inventory, Inventory)

    return m, reader, inventory


# main
if __name__ == "__main__":
    test()


# end of file 
