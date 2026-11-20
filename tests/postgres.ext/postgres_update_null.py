#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that an update can set a field to NULL
"""


def test():
    """
    Clear the fields of a row with an update
    """
    # access the package
    import pyre.db

    # a table with a field of a few types
    class Sample(pyre.db.table, id="pyre_update_null"):
        """
        A row of values that may be cleared
        """

        # the key
        id = pyre.db.int().primary()
        # a string
        name = pyre.db.str()
        # a flag
        flag = pyre.db.bool()
        # and a date
        day = pyre.db.date()

    # connect
    db = pyre.db.postgres(name="updates").attach()
    # in a transaction that leaves nothing behind
    db.execute("BEGIN")
    # carefully
    try:
        # make the table
        db.createTable(Sample)
        # with a row in it whose fields are all set
        db.execute(
            "INSERT INTO pyre_update_null (id, name, flag, day) VALUES (1, 'x', true, '2026-11-19')"
        )
        # build a template that clears them
        template = pyre.db.template(Sample)
        template.name = pyre.db.null
        template.flag = pyre.db.null
        template.day = pyre.db.null
        # apply it
        db.update((template, Sample.id == 1))
        # every field must now be NULL
        found = db.execute(
            "SELECT name IS NULL, flag IS NULL, day IS NULL FROM pyre_update_null WHERE id = 1"
        )
        # so check, accepting the truth whether the bindings spell it as a boolean or as text
        assert tuple(found[0]) in {(True,) * 3, ("t",) * 3}, tuple(found[0])
    # either way
    finally:
        # leave nothing behind
        db.execute("ROLLBACK")
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
