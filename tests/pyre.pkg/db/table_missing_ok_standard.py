#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that standard SQL refuses to drop a table only when it is present
"""


def test():
    """
    Ask the standard mill to drop a table that may be gone, and check it refuses
    """
    # access the package
    import pyre.db

    # a table of things
    class Thing(pyre.db.table, id="things"):
        # the name
        name = pyre.db.str()

    # and its exceptions
    from pyre.db import exceptions

    # make a mill
    mill = pyre.db.backends.standard.mill(name="refusal")
    # attempt to
    try:
        # build the statement
        statement = tuple(mill.dropTable(table=Thing, missingOk=True))
    # which must fail
    except exceptions.NotSupportedError as error:
        # naming what it was asked for
        assert "the table things" in str(error), str(error)
    # if it doesn't
    else:
        # the statement was built anyway
        assert False, statement
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
