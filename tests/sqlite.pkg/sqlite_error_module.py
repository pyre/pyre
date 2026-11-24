#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that the errors of the module that binds sqlite, which carry no code, become pyre.db's
exceptions of the same name
"""


def test():
    """
    Run a statement with fewer values than placeholders, and check the refusal
    """
    # access the package
    import pyre.db

    # connect to a database in memory
    db = pyre.db.sqlite(name="errors").attach()
    # attempt to
    try:
        # run a statement with two placeholders and one value
        db.run("SELECT ?1, ?2", 1)
    # which is refused
    except pyre.db.exceptions.ProgrammingError as error:
        # and the condition has no name from sqlite
        assert error.code == "", error.code
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
