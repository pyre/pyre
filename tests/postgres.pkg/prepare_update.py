#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a prepared update sets the values its slots are given, in the rows its slots pick
"""


def test():
    """
    Prepare an update of the size of a granule, and run it for two granules
    """
    # access the package
    import pyre.db

    # a table of granules
    class Granule(pyre.db.table, id="pyre_prepare_update"):
        """
        Granules
        """

        # the name
        name = pyre.db.str().primary()
        # and the size
        size = pyre.db.int()

    # connect
    db = pyre.db.postgres(name="prepare_update").attach()
    # make the table
    db.createTable(Granule)
    # carefully
    try:
        # add three granules
        db.insert(*(Granule.pyre_immutable(name=name, size=0) for name in "abc"))
        # a template whose size is given when the statement runs
        template = pyre.db.template(Granule)
        template.size = pyre.db.parameter(name="size")
        # prepare the update of the granule whose name is given too
        resize = db.prepareUpdate(
            template=template,
            condition=Granule.name == pyre.db.parameter(name="name", schema=pyre.db.str()),
        )
        # resize the first, which hands back nothing without {returning}
        assert resize.run(name="a", size=10) is None
        # and the last
        resize.run(name="c", size=30)
        # read them back
        sizes = {row.name: row.size for row in db.select(Granule)}
        # the two were resized, and the other was left alone
        assert sizes == {"a": 10, "b": 0, "c": 30}, sizes
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
