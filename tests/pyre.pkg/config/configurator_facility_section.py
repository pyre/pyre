#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
A configuration file can both bind a facility of a component, in the section of its owner, and
configure the part it binds, in a section of its own named after the part: the part is built
from the family the binding names, under the name of the facility, and takes its settings from
its own section, whichever of the two comes first
"""


# the driver
def test() -> None:
    """
    Load a file that binds and configures a part in both orders, and check each part
    """
    # support
    import pyre

    # the protocol of the parts
    class Part(pyre.protocol, family="facility_section.parts"):
        """
        A part
        """

    # a part with a setting
    class Knob(pyre.component, family="facility_section.parts.knob", implements=Part):
        """
        A part that can be turned
        """

        # the setting
        turns = pyre.properties.int()
        turns.default = 0
        turns.doc = "how many times the knob has been turned"

    # the part an owner gets when the file says nothing
    class Plug(pyre.component, family="facility_section.parts.plug", implements=Part):
        """
        A part with no settings
        """

    # the owner of a part
    class Owner(pyre.component, family="facility_section.owners"):
        """
        A component with a part
        """

        # the facility
        part = Part()
        part.default = Plug
        part.doc = "the part of the owner"

    # load the file
    pyre.loadConfiguration("facility_section.yaml")

    # go through the owners and the settings their parts should have
    for name, turns in (("alpha", 7), ("beta", 11)):
        # build the owner
        owner = Owner(name=name)
        # its part is the one the binding names
        assert isinstance(owner.part, Knob), (name, type(owner.part))
        # under the name of the facility
        assert owner.part.pyre_name == f"{name}.part", (name, owner.part.pyre_name)
        # with the settings of its own section
        assert owner.part.turns == turns, (name, owner.part.turns)

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
