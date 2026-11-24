#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that the values of the slots of a prepared statement are converted at every run: by the
column a slot stands for, or by the type of the slot
"""


def test():
    """
    Prepare an update whose new moment is a slot of its column, picking rows by a slot of a size,
    and run it with values given as text
    """
    # support
    import datetime

    # access the package
    import pyre.db

    # a table of granules
    class Granule(pyre.db.table, id="pyre_prepare_types"):
        """
        Granules
        """

        # the name
        name = pyre.db.str().primary()
        # the size
        size = pyre.db.int()
        # and when it was last seen
        seen = pyre.db.timestamp()

    # the moment everything was first seen
    first = datetime.datetime(2026, 11, 1)
    # and the one the update sets
    later = datetime.datetime(2026, 11, 24, 12, 30)
    # connect
    db = pyre.db.postgres(name="prepare_types").attach()
    # make the table
    db.createTable(Granule)
    # carefully
    try:
        # add two granules
        db.insert(
            Granule.pyre_immutable(name="a", size=1, seen=first),
            Granule.pyre_immutable(name="b", size=2, seen=first),
        )
        # a template whose moment is given when the statement runs; the column gives its type
        template = pyre.db.template(Granule)
        template.seen = pyre.db.parameter(name="seen")
        # prepare the update of the granules of the size given too, which says its type
        touch = db.prepareUpdate(
            template=template,
            condition=Granule.size == pyre.db.parameter(name="size", schema=pyre.db.int()),
        )
        # run it with both values as text, which the run converts
        touch.run(seen="2026-11-24 12:30:00", size="2")
        # read the granules back
        seen = {row.name: row.seen for row in db.select(Granule)}
        # only the second was touched, with the moment the text named
        assert seen == {"a": first, "b": later}, seen
    # either way
    finally:
        # leave nothing behind
        db.dropTable(Granule)
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
