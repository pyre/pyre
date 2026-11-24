#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a value the dialect has no type for is refused as a parameter, as it is as a literal
"""


def test():
    """
    Insert a record with an identifier through the dialect of sqlite, and check it is refused
    """
    # support
    import uuid

    # access the package
    import pyre.db

    # a table of things
    class Thing(pyre.db.table, id="things"):
        # an identifier, which sqlite has no type for
        tag = pyre.db.uuid()

    # a thing
    thing = Thing.pyre_immutable(tag=uuid.UUID(int=7))
    # make a mill that speaks the dialect of sqlite
    mill = pyre.db.backends.sqlite.mill(name="parameters")
    # and a place for the values of a statement
    parameters = mill.parameters()
    # attempt to
    try:
        # build the statement
        tuple(mill.insertRecords(thing, parameters=parameters))
    # which is refused
    except pyre.db.exceptions.NotSupportedError as error:
        # with the explanation the literals give
        assert "identifiers" in error.diagnostic, error.diagnostic
    # anything else
    else:
        # is a failure
        assert False, "the identifier was not refused"
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
