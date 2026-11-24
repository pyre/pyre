#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that the refusal to reproduce many tables that refer to each other names a few of them and
counts the rest, so that it stays short
"""


def test():
    """
    Declare five tables that refer to each other in a ring, and ask a server to reproduce them
    """
    # access the package
    import pyre.db

    # five tables, each with a name and the name of a row of the table after it
    class Alpha(pyre.db.table, id="alpha"):
        """
        The first table of the ring
        """

        # the name
        name = pyre.db.str().primary()
        # and the row it refers to
        following = pyre.db.str()

    class Beta(pyre.db.table, id="beta"):
        """
        The second table of the ring
        """

        # the name
        name = pyre.db.str().primary()
        # and the row it refers to
        following = pyre.db.str()

    class Gamma(pyre.db.table, id="gamma"):
        """
        The third table of the ring
        """

        # the name
        name = pyre.db.str().primary()
        # and the row it refers to
        following = pyre.db.str()

    class Delta(pyre.db.table, id="delta"):
        """
        The fourth table of the ring
        """

        # the name
        name = pyre.db.str().primary()
        # and the row it refers to
        following = pyre.db.str()

    class Epsilon(pyre.db.table, id="epsilon"):
        """
        The last table of the ring
        """

        # the name
        name = pyre.db.str().primary()
        # and the row it refers to
        following = pyre.db.str()

    # the tables, in the order of the ring
    tables = (Alpha, Beta, Gamma, Delta, Epsilon)
    # and their names
    names = tuple(table.pyre_name for table in tables)
    # each refers to the one after it, and the last to the first, which closes the ring
    for table, following in zip(tables, tables[1:] + tables[:1]):
        # one at a time
        table.pyre_foreignKey(field=table.following, foreign=following.name)

    # the source, a database in memory with nothing in it
    source = pyre.db.sqlite(name="reproduce_cycle_long_source").attach()
    # the target, a file of statements, named after this driver
    target = pyre.db.backup(name="reproduce_cycle_long", stream="reproduce_cycle_long.sql")
    # carefully
    try:
        # reproduce the tables
        target.reproduce(source=source, tables=tables)
    # it must be refused
    except pyre.db.exceptions.NotSupportedError as error:
        # the explanation
        explanation = str(error)
        # names three of the tables
        assert sum(name in explanation for name in names) == 3, explanation
        # and counts the other two
        assert "2 others" in explanation, explanation
    # if it is not
    else:
        # say so
        assert False, "tables that refer to each other were reproduced"
    # make sure the file is on disk
    target.stream.close()
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
