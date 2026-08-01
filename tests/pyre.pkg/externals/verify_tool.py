#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verification of a tool only category doesn't assume the traits of a library

Tool installations carry {bindir} and their executable traits, but none of the library
geometry; an audit that reaches for {incdir} unconditionally fails on them
"""

# support
import pyre


# the application
class verify_tool(pyre.application):
    """
    An application that verifies its requirements
    """


def test():
    """
    Verify gcc, which is a tool with no headers or libraries
    """
    # instantiate the application; this loads {verify_tool.yaml}
    app = verify_tool(name="verify_tool")
    # resolve the request
    report = pyre.externals.resolve(requested=["gcc"])
    # the fixture provides a compiler front end
    gcc = report.selections["gcc"]
    # which carries no library geometry at all
    assert not hasattr(gcc, "incdir")

    # verify the outcome; this must not trip over the missing traits
    audit = pyre.externals.index().verify(report=report)
    # the executable resolves, so the installation checks out
    assert audit.verified == ["gcc"]
    # with nothing broken
    assert not audit.broken

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
