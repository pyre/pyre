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
    from pyre.config.events import Assignment
    # get the codec manager
    m = pyre.config.newCodecManager()
    # ask for a pml codec
    reader = m.newCodec(encoding="pml")
    # open a stream
    sample = open("sample-package.pml")
    # read the contents
    events = reader.decode(source=sample)
    # check that we got a non-trivial instance
    assert events 

    # verify its contents
    event = events[0]
    assert isinstance(event, Assignment)
    assert tuple(event.key) == ("pyre", "home")
    assert event.value == "pyre.home"

    event = events[1]
    assert isinstance(event, Assignment)
    assert tuple(event.key) == ("pyre", "prefix")
    assert event.value == "pyre.prefix"

    return m, reader, events


# main
if __name__ == "__main__":
    test()


# end of file 
