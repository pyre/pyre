#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verification catches a user configured include path that lacks the header markers

The configuration file {verify_headers.yaml} points the gsl include path at a directory
that exists but holds no headers. Configuration validation is satisfied, since the folder
is there; only re-proving the markers against the effective paths catches it
"""

# support
import pyre


# the application
class verify_headers(pyre.application):
    """
    An application that verifies its requirements
    """


def test():
    """
    Verify gsl against an include path the user pointed somewhere useless
    """
    # instantiate the application; this loads {verify_headers.yaml}
    app = verify_headers(name="verify_headers")
    # resolve the request
    report = pyre.externals.resolve(requested=["gsl"])
    # the installation was found
    gsl = report.selections["gsl"]
    # and the user override took effect
    assert [str(folder) for folder in gsl.incdir] == ["prefix/lib"]
    # the folder exists, so configuration validation has no complaint
    assert not gsl.pyre_configurationErrors

    # verify the outcome
    audit = pyre.externals.index().verify(report=report)
    # the installation is broken
    assert "gsl" in audit.broken
    # because the header marker no longer resolves
    assert any("gsl/gsl_version.h" in complaint for complaint in audit.broken["gsl"])
    # so it is not among the verified
    assert "gsl" not in audit.verified
    # and the audit is not clean
    assert not audit.clean

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
