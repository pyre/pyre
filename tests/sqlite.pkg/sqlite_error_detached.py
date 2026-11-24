#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a statement sent through a server that is not attached is refused as a misuse of the
interface
"""


def test():
    """
    Send a statement through a server that was never attached, and check the refusal
    """
    # access the package
    import pyre.db

    # make a server, and leave it detached
    db = pyre.db.sqlite(name="detached")
    # attempt to
    try:
        # run a statement through it
        db.execute("SELECT 1;")
    # which is refused
    except pyre.db.exceptions.InterfaceError as error:
        # with an explanation
        assert error.diagnostic == "this server is not attached", error.diagnostic
    # anything else
    else:
        # is a failure
        assert False, "the statement was not refused"
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
