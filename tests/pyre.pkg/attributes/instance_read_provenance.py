#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that reading a facility leaves the provenance of its value alone
"""


def test() -> None:
    """
    Make an instance, note the priority of its facility, read it, and compare
    """
    # access the framework
    import pyre

    # the store
    nameserver = pyre.executive.nameserver

    # a protocol for tools
    class tool(pyre.protocol, family="pyre.tests.attributes.tools"):
        """the obligations of a tool"""

    # a tool
    class hammer(pyre.component, family="pyre.tests.attributes.tools.hammer", implements=tool):
        """the tool of the class"""

    # another tool
    class saw(pyre.component, family="pyre.tests.attributes.tools.saw", implements=tool):
        """the tool the class switches to"""

    # a component class with a facility
    class base(pyre.component, family="pyre.tests.attributes.base"):
        """a component class with a facility"""

        # the facility, with its class default
        t = tool(default=hammer)

    # an instance
    b = base(name="b")
    # the tool comes from the class, at the rank of a default
    assert b.pyre_how("t").category == nameserver.priority.defaults.category
    # use the tool
    b.t
    # nobody set it, so it still ranks as a default
    assert b.pyre_how("t").category == nameserver.priority.defaults.category

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
