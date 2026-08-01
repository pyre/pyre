#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verification catches a link line naming a library that isn't there

The configuration file {verify_libraries.yaml} adds a library stem to the gsl link line
that no file in the library path provides; the linker would fail on it, and verification
says so first
"""

# support
import pyre


# the application
class verify_libraries(pyre.application):
    """
    An application that verifies its requirements
    """


def test():
    """
    Verify gsl against a link line the user extended with a phantom library
    """
    # instantiate the application; this loads {verify_libraries.yaml}
    app = verify_libraries(name="verify_libraries")
    # resolve the request
    report = pyre.externals.resolve(requested=["gsl"])
    # the user override took effect
    assert list(report.selections["gsl"].libraries) == ["gsl", "gslcblas", "nosuchlib"]

    # verify the outcome
    audit = pyre.externals.index().verify(report=report)
    # the installation is broken
    assert "gsl" in audit.broken
    # because the phantom stem resolves to no file
    assert any("nosuchlib" in complaint for complaint in audit.broken["gsl"])
    # while the real stems drew no complaints
    assert not any("'gsl'" in complaint for complaint in audit.broken["gsl"])

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
