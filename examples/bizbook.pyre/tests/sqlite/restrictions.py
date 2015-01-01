#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
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
        # restrict the results
        where = book.category == "cookbook"

    # build datastore
    db = bizbook.sqlite()

    # run the query
    result = tuple(db.select(titles))
    # there are five cookbooks in the dataset
    assert len(result) == 5
    # make sure that only cookbooks got through
    for record in result:
        assert record.category == 'cookbook'

    return db, titles


# main
if __name__ == "__main__":
    test()


# end of file
