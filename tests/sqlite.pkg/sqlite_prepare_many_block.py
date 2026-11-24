#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a run of a prepared statement that fails among many on sqlite, inside a transaction
block, undoes only its batch, and keeps the batches before it for the block to commit
"""


def test():
    """
    Resize five granules two at a time inside a block, the fourth to a size the table refuses
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

    # whose sizes are never negative
    Granule.pyre_check(Granule.size >= 0)

    # connect to a database in memory, which runs two statements at a time
    db = pyre.db.sqlite(name="prepare_many_block", batch=2).attach()
    # make the table
    db.createTable(Granule)
    # carefully
    try:
        # add five granules
        db.insert(*(Granule.pyre_immutable(name=name, size=0) for name in "abcde"))
        # a template whose size is given when the statement runs
        template = pyre.db.template(Granule)
        template.size = pyre.db.parameter(name="size")
        # prepare the update of the granule whose name is given too
        resize = db.prepareUpdate(
            template=template,
            condition=Granule.name == pyre.db.parameter(name="name", schema=pyre.db.str()),
        )
        # the runs, the fourth of which the table refuses
        runs = [{"name": "a", "size": 1}, {"name": "b", "size": 2}, {"name": "c", "size": 3}]
        # and the last
        runs += [{"name": "d", "size": -4}, {"name": "e", "size": 5}]
        # in a transaction block
        with db:
            # carefully
            try:
                # run them all
                resize.runMany(runs)
            # the failure is expected
            except pyre.db.exceptions.IntegrityError:
                # and the block goes on with what the batches before it did
                pass
            # running to the end
            else:
                # means the failure was lost
                assert False, "the run the table refuses went through"
        # read the sizes back
        sizes = {row.name: row.size for row in db.select(Granule)}
        # the first batch was kept, the second undone, and the third never ran
        assert sizes == {"a": 1, "b": 2, "c": 0, "d": 0, "e": 0}, sizes
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
