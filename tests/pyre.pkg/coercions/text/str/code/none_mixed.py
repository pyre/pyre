#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that assigning the text 'nOnE' to a str trait leaves it unset
"""


def test() -> None:
    """
    Make an instance, set its trait to the text 'nOnE' in code, and read it
    """
    # access the framework
    import pyre

    # a component with a str trait
    class component(pyre.component):
        """a component with a str trait"""

        # the trait
        t = pyre.properties.str()

    # make an instance
    c = component(name="c")
    # set the trait to the text 'nOnE'
    c.t = "nOnE"
    # the setting took effect, at the rank of its source
    assert c.pyre_how(attribute="t").category == pyre.executive.priority.explicit.category
    # the trait is unset
    assert c.t is None

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
