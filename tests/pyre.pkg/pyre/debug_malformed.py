#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
A request to debug modules that is not a collection of module names stops the import of the
framework, rather than being ignored
"""


def test() -> None:
    """
    Import the framework with a malformed debugging request, and check it is not ignored
    """
    # carefully
    try:
        # import the framework
        import pyre
    # the request is not a collection of names
    except TypeError:
        # so it must stop the import
        pass
    # if it is ignored
    else:
        # say so
        assert False, "a malformed debugging request was ignored"

    # all done
    return


# main
if __name__ == "__main__":
    # ask to debug modules, with something that is not a collection of module names
    pyre_debug = 5
    # do...
    test()


# end of file
