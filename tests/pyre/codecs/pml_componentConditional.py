#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


"""
Verify processing of a correct pml input file
"""


def test():
    # package access
    import pyre.config
    from pyre.config.events import Assignment, ConditionalAssignment
    # get the codec manager
    m = pyre.config.newCodecManager()
    # ask for a pml codec
    reader = m.newCodec(encoding="pml")
    # open a stream
    sample = open("sample-componentConditional.pml")
    # read the contents
    events = reader.decode(source=sample)
    # check that we got a non-trivial instance
    assert events

    # verify its contents
    event = events[0]
    assert isinstance(event, ConditionalAssignment)
    assert event.component == ["mine"]
    assert event.conditions == [(["mine"], ["test", "sample"])]
    assert event.key == ["author"]
    assert event.value == "Michael Aïvázis"

    event = events[1]
    assert isinstance(event, ConditionalAssignment)
    assert event.component == ["mine"]
    assert event.conditions == [(["mine"], ["test", "sample"])]
    assert event.key == ["affiliation"]
    assert event.value == "California Institute of Technology"

    return m, reader, events


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    test()


# end of file 
