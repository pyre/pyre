#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that a quote in the pattern of a {LIKE} is doubled, so the pattern stays one string
"""


def test():
    """
    Render a query whose restriction matches a pattern with a quote in it
    """
    # access the package
    import pyre.db

    # a table of streets
    class Street(pyre.db.table, id="streets"):
        """
        Street names
        """

        # the name
        name = pyre.db.str()

    # the streets named after O'Hara
    class OHara(pyre.db.query, street=Street):
        """
        The streets named after O'Hara
        """

        # the field
        name = street.name
        # the restriction
        where = pyre.db.like(street.name, "O'Hara%")

    # get a server
    server = pyre.db.server()
    # generate the statement
    statement = tuple(server.sql.select(OHara))
    # the restriction is the last line, and its pattern is a single string
    assert statement[-1] == "    ((street.name LIKE 'O''Hara%' ESCAPE '\\'));", statement[-1]
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
