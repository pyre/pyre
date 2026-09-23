#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that the help screen of an application lists the options that are not traits: the help
markers of its shell, and the configuration loader
"""

# support
import pyre


# an application with a trait
class app(pyre.application, family="shells.help.app"):
    """
    A sample application
    """

    # a trait, so the options section has something to show
    level = pyre.properties.int(default=1)
    level.doc = "the level"


def test():
    # instantiate
    a = app(name="application_help")
    # render the help screen
    text = "\n".join(a.pyre_help())
    # the trait is there
    assert "--level" in text
    # and so are the special options, in a section of their own
    assert "special options:" in text
    # the help markers of the script shell
    assert "--help" in text
    # and the configuration loader
    assert "--config=" in text
    # all done
    return a


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
