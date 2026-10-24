#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that an instance of a subclass that has read its facility keeps the component it got when
the facility of the parent changes, as with a python cached property
"""


def test() -> None:
    """
    Make an instance of the subclass, read its facility, assign a new component to the class
    facility, and read the instance again
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

    # a subclass that says nothing about the trait
    class derived(base, family="pyre.tests.attributes.derived"):
        """a subclass that inherits the trait"""

    # an instance of the subclass made before the change
    d = derived(name="d")
    # that has used the tool of the class
    tool = d.t
    # which is a hammer
    assert isinstance(tool, hammer)
    # switch the tool of the class
    base.t = saw
    # the instance keeps the tool it has
    assert d.t is tool
    # while an instance made after the change gets the new one
    assert isinstance(derived(name="e").t, saw)

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
