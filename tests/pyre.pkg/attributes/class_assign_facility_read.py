#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that an instance that has read its facility keeps the component it got when the class
facility changes, as with a python cached property
"""


def test() -> None:
    """
    Make an instance, read its facility, assign a new component to the class facility, and read the
    instance again
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

    # an instance made before the change
    b = base(name="b")
    # that has used the tool of the class
    tool = b.t
    # which is a hammer
    assert isinstance(tool, hammer)
    # switch the tool of the class
    base.t = saw
    # the instance keeps the tool it has
    assert b.t is tool
    # while an instance made after the change gets the new one
    assert isinstance(base(name="c").t, saw)

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
