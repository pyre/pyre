#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that setting a str trait to 'none' in a pfg document leaves it unset
"""


def test() -> None:
    """
    Load a pfg document that sets the trait to 'none', make the instance, and read it
    """
    # access the framework
    import pyre

    # and the support for in-memory documents
    import io

    # access the executive
    executive = pyre.executive
    # the document
    document = "c:\n    t = none\n"
    # load it, which must go through without complaint
    assert not executive.configurator.loadConfiguration(
        uri=pyre.primitives.uri.parse("vfs:/none.pfg"),
        source=io.StringIO(document),
        locator=pyre.tracking.simple("the test"),
        priority=executive.priority.user,
    )

    # a component with a str trait
    class component(pyre.component):
        """a component with a str trait"""

        # the trait
        t = pyre.properties.str()

    # make the instance the document configures
    c = component(name="c")
    # the setting took effect, at the rank of its source
    assert c.pyre_how(attribute="t").category == pyre.executive.priority.user.category
    # the trait is unset
    assert c.t is None

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
