#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that the runs of a prepared statement that hands back rows hand back the records of every
run, in the order of the runs
"""


def test():
    """
    Prepare an update that hands back the rows it changes, and run it for three granules
    """
    # access the package
    import pyre.db

    # a table of granules
    class Granule(pyre.db.table, id="pyre_prepare_many_returning"):
        """
        Granules
        """

        # the name
        name = pyre.db.str().primary()
        # and the size
        size = pyre.db.int()

    # connect, running two statements at a time
    db = pyre.db.postgres(name="prepare_many_returning", batch=2).attach()
    # make the table
    db.createTable(Granule)
    # carefully
    try:
        # add three granules
        db.insert(*(Granule.pyre_immutable(name=name, size=0) for name in "abc"))
        # a template whose size is given when the statement runs
        template = pyre.db.template(Granule)
        template.size = pyre.db.parameter(name="size")
        # prepare the update of the granule whose name is given too, which hands back its row
        resize = db.prepareUpdate(
            template=template,
            condition=Granule.name == pyre.db.parameter(name="name", schema=pyre.db.str()),
            returning=Granule,
        )
        # resize them in reverse
        records = resize.runMany({"name": name, "size": 10} for name in "cba")
        # the records of the runs, in their order
        assert [(record.name, record.size) for record in records] == [
            ("c", 10),
            ("b", 10),
            ("a", 10),
        ], records
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
