#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that the literal of an array writes a null entry as NULL
"""


def test():
    """
    Insert a row with arrays that hold nulls, and check the statement
    """
    # access the package
    import pyre.db

    # a table of samples
    class Sample(pyre.db.table, id="samples"):
        """
        Samples
        """

        # the labels
        labels = pyre.db.array(schema=pyre.db.str())
        # and the cells of a grid
        cells = pyre.db.array(schema=pyre.db.int(), rank=2)

    # make a mill that speaks standard SQL
    mill = pyre.db.backends.standard.mill(name="literals_array_null")
    # build the statement
    statement = tuple(
        mill.insertRecords(Sample.pyre_immutable(labels=("a", None), cells=((1, None), (None, 4))))
    )
    # and check it
    assert statement == (
        "INSERT INTO samples",
        "    (labels, cells)",
        "  VALUES",
        "    (ARRAY['a', NULL], ARRAY[ARRAY[1, NULL], ARRAY[NULL, 4]]);",
    ), statement
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
