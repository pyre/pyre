#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


"""
Verify that we can process an empty pml file
"""


def test():
    # package access
    import pyre.config
    # get the codec manager
    m = pyre.config.newCodecManager()
    # ask for a pml codec
    reader = m.newCodec(encoding="pml")
    # open a stream
    sample = open("sample-empty.pml")
    # read the contents
    configuration = reader.decode(source=sample)
    # check that we got a real instance back
    assert configuration is not None
    # check that it is an instance of the right type
    assert isinstance(configuration, reader.Configuration)

    return m, reader, configuration


# main
if __name__ == "__main__":
    test()


# end of file 
