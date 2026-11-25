#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that the keys a derived table inherits name the columns it redeclares
"""


def test():
    """
    Derive a table that redeclares the columns its base uses in its keys and indexes, and check
    that the derived table applies them to the redeclared columns
    """
    # access the package
    import pyre.db

    # a table of people
    class Person(pyre.db.table, id="persons"):
        """
        People
        """

        # the key
        id = pyre.db.int()
        # and the name, of any length
        name = pyre.db.str()

    # the key identifies people
    Person.pyre_primaryKey(Person.id)
    # no two people share a name
    Person.pyre_unique(Person.name)
    # and people are looked up by name
    Person.pyre_index(Person.name)

    # a table of people with short names, known by their badge numbers
    class Badge(Person, id="badges"):
        """
        People whose names fit on a badge
        """

        # the badge number
        id = pyre.db.str(maxlen=4)
        # and the name, short enough to fit
        name = pyre.db.str(maxlen=8)

    # the primary key of the derived table has one field
    assert len(Badge._pyre_primaryKeys) == 1
    # its own key
    assert Badge._pyre_primaryKeys[0] is Badge.id.field
    # it has one unique group
    ((fields, _),) = Badge._pyre_uniqueKeys
    # made of its own name
    assert len(fields) == 1 and fields[0] is Badge.name.field
    # and one index
    (index,) = Badge._pyre_indexes
    # over its own name too
    assert len(index.fields) == 1 and index.fields[0] is Badge.name.field

    # while the base keeps its own
    assert Person._pyre_primaryKeys[0] is Person.id.field

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
