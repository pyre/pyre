#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that the pattern of a match, and its escape character, are parameters
"""


def test():
    """
    Match a field against a pattern, and check the pattern and the escape are placeholders
    """
    # access the package
    import pyre.db

    # a table of readings
    class Reading(pyre.db.table, id="readings"):
        # the city
        city = pyre.db.str()
        # the day of the reading
        day = pyre.db.date()
        # and how many there were
        count = pyre.db.int()

    # make a mill that speaks the dialect of postgres
    mill = pyre.db.backends.postgres.mill(name="parameters")
    # and a place for the values of a statement
    parameters = mill.parameters()
    # the cities whose name starts with a quote
    predicate = pyre.db.like(Reading.city, "O'%")
    # render it
    text = mill.expression(root=predicate, context=Reading, parameters=parameters)
    # the pattern and the escape character are placeholders of text
    assert text == "(city LIKE CAST($1 AS TEXT) ESCAPE CAST($2 AS TEXT))", text
    # and travel beside the statement
    assert parameters.drain() == ("O'%", "\\")
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
