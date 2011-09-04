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
    from pyre.config.events import ConditionalAssignment
    # get the codec manager
    m = pyre.config.newCodecManager()
    # ask for a pml codec
    reader = m.newCodec(encoding="pml")
    # open a stream
    sample = open("sample-componentConditionalNested.pml")
    # read the contents
    events = reader.decode(source=sample)
    # check that we got a non-trivial instance
    assert events

    # verify its contents
    event = events[0]
    assert isinstance(event, ConditionalAssignment)
    assert event.component == ["sample", "engine"]
    assert event.conditions == [
        (['sample', 'engine'], ['test', 'part']),
        (['sample'], ['test', 'item'])
        ]
    assert event.key == ["id"]
    assert event.value == '3Q4XYZ'

    return m, reader, events


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    test()


# end of file 
