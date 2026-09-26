#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify processing of a {pfg} input file with conditional assignments whose keys reach
inside a nested component

The key of a conditional assignment is the naked name of the trait, and the rest of the
path names the component that receives it: the nested component, not the one that owns the
constraints. This must be true regardless of whether the path is spelled as a dotted name or
as a nested section, and it matches what the other codecs produce.
"""


def test():
    # package access
    import pyre.config
    from pyre.config.events import Assignment, ConditionalAssignment

    # get the codec manager
    m = pyre.config.newConfigurator()
    # ask for a {pfg} codec
    reader = m.codec(encoding="pfg")
    # the configuration file
    uri = "sample-componentConditionalMultilevel.pfg"
    # open a stream
    sample = open(uri)
    # read the contents
    events = tuple(reader.decode(uri=uri, source=sample, locator=None))
    # check that we got a non-trivial instance
    assert events
    # and that we got them all
    assert len(events) == 5

    # the facility binding is an unconditional assignment with a fully qualified key
    event = events[0]
    assert isinstance(event, Assignment)
    assert event.key == ["subject", "field"]
    assert event.value == "basic#dotted"

    # a single level key in a conditional assignment names a trait of the component
    event = events[1]
    assert isinstance(event, ConditionalAssignment)
    assert event.component == ["dotted"]
    assert event.conditions == [(["dotted"], ["test", "fields", "basic"])]
    assert event.key == ["alias"]
    assert event.value == "dotted_alias"

    # a dotted key reaches inside a nested component, which receives the assignment as long
    # as its owner satisfies the constraint
    event = events[2]
    assert isinstance(event, ConditionalAssignment)
    assert event.component == ["dotted", "discretization"]
    assert event.conditions == [(["dotted"], ["test", "fields", "basic"])]
    assert event.key == ["basis_order"]
    # pfg values are strings; the trait converts them when the assignment lands
    assert event.value == "2"

    # repeat for the component configured using a nested section
    event = events[3]
    assert isinstance(event, ConditionalAssignment)
    assert event.component == ["nested"]
    assert event.conditions == [(["nested"], ["test", "fields", "basic"])]
    assert event.key == ["alias"]
    assert event.value == "nested_alias"

    # the nested section spelling must produce exactly the same event as the dotted one
    event = events[4]
    assert isinstance(event, ConditionalAssignment)
    assert event.component == ["nested", "discretization"]
    assert event.conditions == [(["nested"], ["test", "fields", "basic"])]
    assert event.key == ["basis_order"]
    assert event.value == "3"

    # all done
    return m, reader, events


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    test()


# end of file
