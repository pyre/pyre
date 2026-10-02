#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that an application whose class has no family, and hence no package, can be instantiated
when the script that launched it cannot be found, e.g. after a change of directory from a launch
with a relative path
"""


def test():
    # support
    import sys

    # get access to the framework
    import pyre

    # declare a trivial application with no family
    class application(pyre.application):
        """A trivial pyre application without a package"""

    # remember how this script was launched
    argv0 = sys.argv[0]
    # make the launching script unreachable, so the application cannot find its prefix through it
    sys.argv[0] = "./no-such-script.py"
    # carefully
    try:
        # instantiate
        app = application(name="app")
    # in any case
    finally:
        # restore the launch path
        sys.argv[0] = argv0
    # with neither a script nor a package to go by, the application has no prefix
    assert app.pyre_prefix is None
    # all done
    return app


# main
if __name__ == "__main__":
    test()


# end of file
