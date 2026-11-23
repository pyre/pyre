#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that the membership of a field in a list of strings quotes each of them
"""


def test():
    """
    Test a field against a list of strings, and check its rendering
    """
    # access the package
    import pyre.db

    # a table of granules
    class Granule(pyre.db.table, id="granules"):
        # the name
        name = pyre.db.str()
        # the day of the acquisition
        day = pyre.db.date()
        # the track
        track = pyre.db.int()
        # the lowest elevation
        low = pyre.db.float()
        # and the highest
        high = pyre.db.float()

    # make a mill
    mill = pyre.db.backends.standard.mill(name="predicates")
    # the granules with one of two names
    predicate = pyre.db.isIn(Granule.name, ["first", "the other's"])
    # render it as a check of the table would
    text = mill.expression(root=predicate, context=Granule)
    # and check it
    assert text == "name IN ('first', 'the other''s')", text
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
