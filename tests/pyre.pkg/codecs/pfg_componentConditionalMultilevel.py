#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test():
    """
    Verify processing of a {pfg} input file with conditional assignments whose keys reach
    inside a nested component

    The key of a conditional assignment is the naked name of the trait, and the rest of the
    path names the component that receives it: the nested component, not the one that owns the
    constraints. This must be true regardless of whether the path is spelled as a dotted name or
    as a nested section, and it matches what the other codecs produce.
    """
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
    with open(uri) as sample:
        # and read the contents
        events = tuple(reader.decode(uri=uri, source=sample, locator=None))
    # check that we got a non-trivial instance
    assert events
    # and that we got them all
    assert len(events) == 5

    # the facility binding
    event = events[0]
    # is an unconditional assignment
    assert isinstance(event, Assignment)
    # with a fully qualified key
    assert event.key == ["subject", "field"]
    # whose value names the component it binds
    assert event.value == "basic#dotted"

    # a single level key in a conditional assignment
    event = events[1]
    # is a conditional assignment
    assert isinstance(event, ConditionalAssignment)
    # to the component itself
    assert event.component == ["dotted"]
    # as long as it is a basic field
    assert event.conditions == [(["dotted"], ["test", "fields", "basic"])]
    # and it names a trait of the component
    assert event.key == ["alias"]
    # along with its value
    assert event.value == "dotted_alias"

    # a dotted key reaches inside a nested component, which receives the assignment as long
    # as its owner satisfies the constraint
    event = events[2]
    # so it is a conditional assignment
    assert isinstance(event, ConditionalAssignment)
    # to the nested component
    assert event.component == ["dotted", "discretization"]
    # under the constraint on its owner
    assert event.conditions == [(["dotted"], ["test", "fields", "basic"])]
    # of the naked trait name
    assert event.key == ["basis_order"]
    # and its value, a string, since pfg values are strings that the trait converts
    # when the assignment lands
    assert event.value == "2"

    # repeat for the component configured using a nested section
    event = events[3]
    # it is a conditional assignment
    assert isinstance(event, ConditionalAssignment)
    # to the component itself
    assert event.component == ["nested"]
    # as long as it is a basic field
    assert event.conditions == [(["nested"], ["test", "fields", "basic"])]
    # of one of its traits
    assert event.key == ["alias"]
    # and its value
    assert event.value == "nested_alias"

    # the nested section spelling must produce exactly the same event as the dotted one
    event = events[4]
    # a conditional assignment
    assert isinstance(event, ConditionalAssignment)
    # to the nested component
    assert event.component == ["nested", "discretization"]
    # under the constraint on its owner
    assert event.conditions == [(["nested"], ["test", "fields", "basic"])]
    # of the naked trait name
    assert event.key == ["basis_order"]
    # and its value, a string
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
