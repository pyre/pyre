#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that one insert may put rows into several tables of a sqlite database
"""


def test():
    """
    Insert into two tables at once
    """
    # access the package
    import pyre.db

    # a table of cats
    class Cat(pyre.db.table, id="cats"):
        """
        Cats
        """

        # the name
        name = pyre.db.str()

    # and one of dogs
    class Dog(pyre.db.table, id="dogs"):
        """
        Dogs
        """

        # the name
        name = pyre.db.str()

    # connect to a database in memory
    db = pyre.db.sqlite(name="pets").attach()
    # make the table of cats
    db.createTable(Cat)
    # and the table of dogs
    db.createTable(Dog)
    # put a row in each, at once
    db.insert(Cat.pyre_immutable(name="tom"), Dog.pyre_immutable(name="rex"))
    # the cat is there
    assert [row.name for row in db.select(Cat)] == ["tom"]
    # and so is the dog
    assert [row.name for row in db.select(Dog)] == ["rex"]
    # let go
    db.detach()
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
