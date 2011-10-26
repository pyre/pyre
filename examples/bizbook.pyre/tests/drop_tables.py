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

    # drop the tables
    db.dropTable(bizbook.schema.Editor)
    db.dropTable(bizbook.schema.Author)
    db.dropTable(bizbook.schema.Book)
    db.dropTable(bizbook.schema.Staff)
    db.dropTable(bizbook.schema.ContactMethod)
    db.dropTable(bizbook.schema.Address)
    db.dropTable(bizbook.schema.Publisher)
    db.dropTable(bizbook.schema.Person)
    db.dropTable(bizbook.schema.Location)

    # and return the component
    return db


# main
if __name__ == "__main__":
    test()


# end of file 
