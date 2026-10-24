#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that reading a facility hands back the same component every time
"""


def test() -> None:
    """
    Make an instance and read its facility twice
    """
    # access the framework
    import pyre

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
    # reading its tool twice gets the same component
    assert b.t is b.t

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
