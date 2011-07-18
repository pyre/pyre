#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


"""
Exercise inserting rows in tables
"""


def test():
    # access the package
    import pyre.db

    # declare the customer table
    class Customer(pyre.db.table, id='customers'):
        """
        Simple customer table
        """
        # the data fields
        cid = pyre.db.int().primary()
        name = pyre.db.str().notNull()
        phone = pyre.db.str(maxlen=10).notNull()
        balance = pyre.db.decimal(precision=7, scale=2).setDefault(0)


    # create some customers
    customers = [
        Customer()
        ]

    # get a server
    server = pyre.db.server(name="test")

    # generate the SQL statement that creates the customer table
    stmt = tuple(server.sql.insert(*customers))
    print('\n'.join(stmt))

    return


# main
if __name__ == "__main__":
    test()


# end of file 
