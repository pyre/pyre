#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


"""
Verify processing of a correct pml input file
"""


def test():
    # package access
    import pyre.config
    # get the codec manager
    m = pyre.config.newCodecManager()
    # ask for a pml codec
    reader = m.newCodec(encoding="pml")
    # open a stream
    sample = open("sample-componentFamily.pml")
    # read the contents
    configuration = reader.decode(source=sample)
    # check that we got a non-trivial instance
    assert configuration is not None
    # check that it is an instance of the right type
    assert isinstance(configuration, reader.Configuration)

    # verify its contents
    event = configuration.events[0]
    assert isinstance(event, configuration.Assignment)
    assert tuple(event.key) == ("test", "sample", "author")
    assert event.value == "Michael Aïvázis"

    event = configuration.events[1]
    assert isinstance(event, configuration.Assignment)
    assert tuple(event.key) == ("test", "sample", "affiliation")
    assert event.value == "California Institute of Technology"

    return m, reader, configuration


# main
if __name__ == "__main__":
    test()


# end of file 
