#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a server refuses to reproduce tables whose foreign keys refer to each other in a
cycle, since no order of the tables lets each one find the rows it refers to
"""


def test():
    """
    Declare two tables that refer to each other, and ask a server to reproduce them
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
        # and the observation that made it
        observation = pyre.db.str()

    # a table of observations
    class Observation(pyre.db.table, id="observations"):
        """
        Observations
        """

        # the name
        name = pyre.db.str().primary()
        # and the first of its granules
        first = pyre.db.str().references(key=Granule.name)

    # the granules refer to their observations, which closes the cycle
    Granule.pyre_foreignKey(field=Granule.observation, foreign=Observation.name)

    # the source, a database in memory with nothing in it
    source = pyre.db.sqlite(name="reproduce_cycle_source").attach()
    # the target, a file of statements, named after this driver
    target = pyre.db.backup(name="reproduce_cycle", stream="reproduce_cycle.sql")
    # carefully
    try:
        # reproduce the tables
        target.reproduce(source=source, tables=(Granule, Observation))
    # it must be refused
    except pyre.db.exceptions.NotSupportedError as error:
        # naming the tables of the cycle
        assert "granules" in str(error) and "observations" in str(error), str(error)
    # if it is not
    else:
        # say so
        assert False, "tables that refer to each other were reproduced"
    # make sure the file is on disk
    target.stream.close()
    # nothing was written
    with open("reproduce_cycle.sql") as stream:
        # so it is empty
        assert stream.read() == ""
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
