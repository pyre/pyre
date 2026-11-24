#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a statement sqlite cannot parse is refused as a programming error, as postgres
refuses it
"""


def test():
    """
    Execute a misspelled statement, and check the refusal
    """
    # access the package
    import pyre.db

    # connect to a database in memory
    db = pyre.db.sqlite(name="errors").attach()
    # attempt to
    try:
        # execute a statement with a misspelled keyword
        db.execute("SELEC 1;")
    # which is refused
    except pyre.db.exceptions.ProgrammingError as error:
        # with sqlite's own name for the condition
        assert error.code == "SQLITE_ERROR", error.code
    # anything else
    else:
        # is a failure
        assert False, "the statement was not refused"
    # disconnect
    db.detach()
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
