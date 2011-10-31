#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


"""
Sanity check: verify that the package is accessible
"""


def test():
    # access the packages
    import pyre.db
    import bizbook

    # access the Book declaration
    Book = bizbook.schema.Book

    # build a simple projection
    class titles(pyre.db.query):
        """A short query on the book table"""
        id = Book.id
        title = Book.title
        category = Book.category
        price = Book.price

    # build datastore
    db = bizbook.pg()

    # run the query
    for record in db.select(titles):
        print("{}: {!r}, {}, {}".format(*record))

    return


# main
if __name__ == "__main__":
    test()


# end of file 
