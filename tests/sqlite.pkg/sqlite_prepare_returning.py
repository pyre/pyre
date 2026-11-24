#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a prepared update with {returning} hands back the rows it changed, as records
"""


def test():
    """
    Prepare an update of the size of a granule that returns it, and run it
    """
    # access the package
    import pyre.db

    # a table of granules
    class Granule(pyre.db.table, id="granules"):
        """
        Granules
        """

        # the name
        name = pyre.db.str().primary()
        # and the size
        size = pyre.db.int()

    # connect to a database in memory
    db = pyre.db.sqlite(name="prepare_returning").attach()
    # make the table
    db.createTable(Granule)
    # with two granules
    db.insert(*(Granule.pyre_immutable(name=name, size=0) for name in "ab"))
    # a template whose size is given when the statement runs
    template = pyre.db.template(Granule)
    template.size = pyre.db.parameter(name="size")
    # prepare the update of the granule whose name is given too, returning it
    resize = db.prepareUpdate(
        template=template,
        condition=Granule.name == pyre.db.parameter(name="name", schema=pyre.db.str()),
        returning=Granule,
    )
    # resize one
    rows = resize.run(name="b", size=7)
    # it comes back, with its new size
    assert [(row.name, row.size) for row in rows] == [("b", 7)], rows
    # disconnect
    db.detach()
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
