#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that the dialect of sqlite refuses a cast to identifiers, which it has no type for, and
says so
"""


def test():
    """
    Render a cast of the code of a thing to an identifier
    """
    # access the package
    import pyre.db

    # and its exceptions
    from pyre.db import exceptions

    # a table of things
    class Thing(pyre.db.table, id="things"):
        """
        Things, by code
        """

        # the code
        code = pyre.db.str()

    # the code of a thing, as an identifier
    tag = pyre.db.cast(Thing.code, pyre.db.uuid())

    # make a mill that speaks the dialect of sqlite
    mill = pyre.db.backends.sqlite.mill(name="expressions_cast_refused")
    # attempt to
    try:
        # render the cast in the context of its table
        expression = mill.expression(root=tag, context=Thing)
    # which must fail
    except exceptions.NotSupportedError as error:
        # with an explanation that names the cast
        assert str(error) == "a cast to identifiers, which sqlite has no type for", str(error)
        # and no table
        assert error.table == "", error.table
        # or column
        assert error.column == "", error.column
    # if it doesn't
    else:
        # the cast was rendered anyway
        assert False, expression
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
