#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a value whose type has no literal in standard SQL is refused, with an explanation
"""


def test():
    """
    Render a query that compares a field to a complex number
    """
    # access the package
    import pyre.db

    # and its exceptions
    from pyre.db import exceptions

    # a table of readings
    class Reading(pyre.db.table, id="readings"):
        """
        Values
        """

        # the value
        value = pyre.db.int()

    # the readings of interest
    class Selected(pyre.db.query, reading=Reading):
        """
        The readings of interest
        """

        # the field
        value = reading.value
        # the restriction
        where = reading.value == 1j

    # make a mill that speaks standard SQL
    mill = pyre.db.dialects.standard(name="literals_where_refused")
    # attempt to
    try:
        # generate the statement
        statement = tuple(mill.select(Selected))
    # which must fail
    except exceptions.NotSupportedError as error:
        # and say why
        assert str(error) == "standard SQL has no literal for values of type complex", str(error)
    # if it doesn't
    else:
        # the value was written anyway
        assert False, statement
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
