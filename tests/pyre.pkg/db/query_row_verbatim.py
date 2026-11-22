#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a row of a query takes its values as they are, without reading them as settings
"""


def test():
    """
    Build a row of a query whose text reads like the name of nothing
    """
    # access the package
    import pyre.db

    # a table of people
    class Person(pyre.db.table, id="persons"):
        """
        People, by name
        """

        # the name
        name = pyre.db.str()

    # their names
    class Names(pyre.db.query, person=Person):
        """
        The names of the people
        """

        # the name
        name = person.name

    # build a row whose name is the text "None"
    row = Names.pyre_immutable(data=("None",))
    # it stays text
    assert row.name == "None", row.name
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
