#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that the negation of a match against a pattern is written with NOT
"""


def test():
    """
    Negate a match, and check its rendering
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
    # the granules whose names do not start with the mission's
    predicate = pyre.db.negation(pyre.db.like(Granule.name, "NISAR%"))
    # render it as a check of the table would
    text = mill.expression(root=predicate, context=Granule)
    # and check it
    assert text == "NOT ((name LIKE 'NISAR%' ESCAPE '\\'))", text
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
