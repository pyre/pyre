#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
An installation whose markers all resolve verifies clean

The configuration file {verify_clean.yaml} restricts the host to the bare engine over the
fixture installation, whose artifacts are all where the gsl recipe expects them
"""

# support
import pyre


# the application
class verify_clean(pyre.application):
    """
    An application that verifies its requirements
    """


def test():
    """
    Resolve and verify gsl against the fixture installation
    """
    # instantiate the application; this loads {verify_clean.yaml}
    app = verify_clean(name="verify_clean")
    # verify the request
    audit = pyre.externals.verify(requested=["gsl"])
    # the installation checks out
    assert audit.verified == ["gsl"]
    # with nothing broken
    assert not audit.broken
    # and the audit as a whole is clean
    assert audit.clean

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
