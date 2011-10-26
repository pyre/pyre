#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


"""
Instantiate the postgres component
"""


def test():
    # import journal
    # journal.debug("postgres.init").active = True
    # journal.debug("postgres.execute").active = True
    # journal.debug("postgres.connection").active = True

    # access the postgres package
    import postgres

    # build a database component
    db = postgres.server(name="bizbook")
    # connect to the default database
    db.attach()

    # get the bizbook schema
    import bizbook

    # build the tables
    db.createTable(bizbook.schema.Location)
    db.createTable(bizbook.schema.Person)
    db.createTable(bizbook.schema.Publisher)
    db.createTable(bizbook.schema.Address)
    db.createTable(bizbook.schema.ContactMethod)
    db.createTable(bizbook.schema.Staff)
    db.createTable(bizbook.schema.Book)
    db.createTable(bizbook.schema.Author)
    db.createTable(bizbook.schema.Editor)

    # and return the component
    return db


# main
if __name__ == "__main__":
    test()


# end of file 
