#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a prepared statement runs once for each of many sets of values, a few runs at a time
"""


def test():
    """
    Prepare an update of the size of a granule, and run it for five granules, two at a time
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

    # connect to a database in memory, which runs two statements at a time
    db = pyre.db.sqlite(name="prepare_many", batch=2).attach()
    # make the table
    db.createTable(Granule)
    # with five granules
    db.insert(*(Granule.pyre_immutable(name=name, size=0) for name in "abcde"))
    # a template whose size is given when the statement runs
    template = pyre.db.template(Granule)
    template.size = pyre.db.parameter(name="size")
    # prepare the update of the granule whose name is given too
    resize = db.prepareUpdate(
        template=template,
        condition=Granule.name == pyre.db.parameter(name="name", schema=pyre.db.str()),
    )
    # resize them all, which hands back nothing without {returning}
    assert resize.runMany({"name": name, "size": size} for size, name in enumerate("abcde")) is None
    # read them back
    sizes = {row.name: row.size for row in db.select(Granule)}
    # every one was resized
    assert sizes == {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4}, sizes
    # disconnect
    db.detach()
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
