#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
A component instance built with a name claims the node at that name, whatever was set there
before, and records the value it set aside; later assignments to the name compete by priority as
usual, the instance a facility builds takes the node of the facility's slot without a word, and an
instance named after a trait of another component fires a firewall
"""


def test() -> None:
    """
    Build named instances where values were set, and check who holds each name
    """
    # support
    import journal
    import pyre

    # the errors are logged as they are recorded; keep the log out of the way
    journal.warning("pyre.configuration").device = journal.trash()
    # get the store
    nameserver = pyre.executive.nameserver
    # the family of the components
    family = "pyre.tests.components.claim"

    # a protocol for a facility
    class Part(pyre.protocol, family=f"{family}.parts"):
        """
        The protocol of the facility
        """

    # and a component that implements it
    class Piece(pyre.component, family=f"{family}.parts.piece", implements=Part):
        """
        The component the facility builds
        """

        # a trait
        x = pyre.properties.int()
        x.default = 1
        x.doc = "an int"

    # a component with a trait and a facility
    class Probe(pyre.component, family=family):
        """
        A component with a trait and a facility
        """

        # the trait
        x = pyre.properties.int()
        x.default = 1
        x.doc = "an int"

        # the facility
        part = Part()
        part.default = Piece
        part.doc = "a facility"

    # a value at the name of an instance, made before the instance is built
    nameserver["first"] = "5"
    # and a setting below it, for its trait
    nameserver["first.x"] = "2"
    # build the instance
    first = Probe(name="first")
    # the instance holds the name
    assert nameserver["first"] is first
    # and is configured by the setting below it
    assert first.x == 2
    # the value it set aside is recorded against it
    recorded = first.pyre_configurationErrors
    # once
    assert len(recorded) == 1, [str(error) for error in recorded]
    # naming the setting and where it was made, which is this file
    assert "'first'" in str(recorded[0]), recorded[0]
    assert "component_instance_name.py" in str(recorded[0]), recorded[0]

    # later, an assignment to the name at a lower priority than the instance's
    nameserver.insert(
        name="first", value="6", priority=nameserver.priority.boot(), locator=pyre.tracking.here()
    )
    # loses, as usual
    assert nameserver["first"] is first
    # while one at a higher priority
    nameserver.insert(
        name="first", value="7", priority=nameserver.priority.user(), locator=pyre.tracking.here()
    )
    # wins, as usual
    assert nameserver["first"] == "7"
    # and neither is recorded against the instance
    assert len(first.pyre_configurationErrors) == 1

    # an instance whose name nobody set
    second = Probe(name="second")
    # holds its name
    assert nameserver["second"] is second
    # and has nothing recorded against it
    assert second.pyre_configurationErrors == []

    # a facility set by the user, at user priority, as a file or the command line would
    nameserver.insert(
        name="third.part",
        value=f"{family}.parts.piece",
        priority=nameserver.priority.user(),
        locator=pyre.tracking.here(),
    )
    # build the instance with the facility
    third = Probe(name="third")
    # reading the facility builds the instance of the component it names
    piece = third.part
    # which is named after the slot of the facility
    assert piece.pyre_name == "third.part"
    # and holds the name of the slot
    assert nameserver["third.part"] is piece
    # without a word against either instance
    assert third.pyre_configurationErrors == []
    assert piece.pyre_configurationErrors == []

    # an instance named after a trait of another component is a bug, so the framework fires a
    # firewall; keep its report out of the way
    journal.firewall("pyre.configuration").device = journal.trash()
    # attempt to
    try:
        # build an instance with the name of the trait {x} of {first}
        Piece(name="second.x")
    # if the firewall fires
    except journal.FirewallError as error:
        # its report names the trait
        assert "'second.x'" in "\n".join(error.page), error.page
    # otherwise
    else:
        # complain
        assert False, "an instance took the name of a trait"
    # and the trait keeps its value
    assert second.x == 1

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
