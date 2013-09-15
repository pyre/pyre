#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2013 all rights reserved
#


"""
Exercise inserting rows in tables
"""


def test():
    # access the package
    import pyre.db

    # declare the person table
    class Person(pyre.db.table, id='persons'):

        id = pyre.db.int().primary()
        name = pyre.db.str().notNull()
        phone = pyre.db.str(maxlen=10).notNull()
        weight = pyre.db.float().notNull()

    # declare the customer table
    class Customer(pyre.db.table, id='customers'):
        """
        Simple customer table
        """
        # the data fields
        cid = pyre.db.int().primary()
        pid = pyre.db.reference(key=Person.id)
        balance = pyre.db.decimal(precision=7, scale=2).setDefault(0)


    # create some customers
    customers = [
        Person.pyre_immutable(id=107, name="Bit Twiddle", phone="+1 800 555 1114", weight=185),
        Person.pyre_immutable(id=108, name="Eva Lu Ator", phone="+1 800 555 7687", weight=112),
        Customer.pyre_immutable(cid=1023, pid=107, balance=1000),
        Customer.pyre_immutable(cid=1024, pid=108, balance=50),
        ]

    # get a server
    server = pyre.db.server(name="test")

    # generate the SQL statement that creates the customer table
    stmt = tuple(server.sql.insertRecords(*customers))
    # print('\n'.join(stmt))
    assert stmt == (
        "INSERT INTO persons",
        "    (id, name, phone, weight)",
        "  VALUES",
        "    (107, 'Bit Twiddle', '+1 800 555 1114', 185.0),",
        "    (108, 'Eva Lu Ator', '+1 800 555 7687', 112.0);",
        "INSERT INTO customers",
        "    (cid, pid, balance)",
        "  VALUES",
        "    (1023, 107, 1000),",
        "    (1024, 108, 50);",
        )

    return


# main
if __name__ == "__main__":
    test()


# end of file 
