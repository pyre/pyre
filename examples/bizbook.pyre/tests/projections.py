#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


"""
Sanity check: verify that the package is accessible
"""


def test():
    # access the packages
    import pyre.db
    import bizbook


    # build a simple projection
    class titles(pyre.db.query, book=bizbook.schema.Book):
        """A short query on the book table"""
        id = book.id
        title = book.title
        category = book.category
        price = book.price

    # build datastore
    db = bizbook.pg()

    # run the query
    for record in db.select(titles):
        # check the length
        assert len(record) == 4
        assert len(record.pyre_entries) == 4
        # check the fields
        assert hasattr(record, 'id')
        assert hasattr(record, 'title')
        assert hasattr(record, 'category')
        assert not hasattr(record, 'publisher')
        assert not hasattr(record, 'date')
        assert not hasattr(record, 'advance')
        assert hasattr(record, 'price')
        assert not hasattr(record, 'description')

    return db, titles


# main
if __name__ == "__main__":
    test()


# end of file 
