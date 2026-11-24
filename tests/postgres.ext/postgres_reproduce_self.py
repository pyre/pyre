#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that reproducing a table whose rows refer to other rows of the same table succeeds when a
row refers to one that comes after it, in a batch of its own
"""


def test():
    """
    Reproduce four granules two at a time, the first of which was derived from the last
    """
    # access the package
    import pyre.db

    # a table of granules
    class Granule(pyre.db.table, id="pyre_reproduce_self"):
        """
        Granules
        """

        # the name
        name = pyre.db.str().primary()
        # and the granule it was derived from, if any
        source = pyre.db.str()

    # the granules refer to the granules they were derived from
    Granule.pyre_foreignKey(field=Granule.source, foreign=Granule.name)

    # the source, a sqlite database in memory
    source = pyre.db.sqlite(name="reproduce_self_source").attach()
    # with the table
    source.createTable(Granule)
    # and four granules, the first derived from the last, so that it refers to a row after it
    source.insert(
        Granule.pyre_immutable(name="a", source="d"),
        Granule.pyre_immutable(name="b", source=None),
        Granule.pyre_immutable(name="c", source="b"),
        Granule.pyre_immutable(name="d", source=None),
    )
    # the target, which writes two rows at a time, so the last row is in a later batch
    target = pyre.db.postgres(name="reproduce_self", batch=2).attach()
    # carefully
    try:
        # reproduce the table
        target.reproduce(source=source, tables=(Granule,))
        # read the granules back
        derived = {row.name: row.source for row in target.select(query=Granule)}
        # they are all there, with their sources
        assert derived == {"a": "d", "b": None, "c": "b", "d": None}, derived
    # either way
    finally:
        # leave nothing behind
        target.dropTable(Granule, missingOk=True)
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
