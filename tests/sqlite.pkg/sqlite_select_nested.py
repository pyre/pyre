#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a selection hands back every row, even when other statements run while it is read
"""


def test():
    """
    Read the granules of a table, writing a note for each one as it arrives
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

    # and one of notes about them
    class Note(pyre.db.table, id="notes"):
        """
        Notes
        """

        # the text
        text = pyre.db.str()

    # connect to a database in memory
    db = pyre.db.sqlite(name="select_nested").attach()
    # make the table of granules
    db.createTable(Granule)
    # and the one of notes
    db.createTable(Note)
    # with five granules
    db.insert(*(Granule.pyre_immutable(name=name) for name in "abcde"))
    # the names that were read
    names = []
    # go through the granules
    for granule in db.select(query=Granule):
        # keep the name
        names.append(granule.name)
        # and write a note about it
        db.insert(Note.pyre_immutable(text=f"read {granule.name}"))
    # every granule was read
    assert sorted(names) == list("abcde"), names
    # and every one got its note
    assert len(list(db.select(query=Note))) == 5
    # disconnect
    db.detach()
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
