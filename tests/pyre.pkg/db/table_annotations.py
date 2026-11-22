#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Exercise attaching constraints to tables
"""


def test():
    """
    Declare two tables with keys, a uniqueness constraint and checks, and render them
    """
    # access the package
    import pyre.db

    # declare the customer table
    class Customer(pyre.db.table, id="customers"):
        """
        Simple customer table
        """

        # the identifier of the customer
        cid = pyre.db.int()
        cid.doc = "the customer id"
        # their name, which is required
        name = pyre.db.str().notNull()
        # their phone number
        phone = pyre.db.str(maxlen=10)
        # and how much they owe
        balance = pyre.db.decimal(precision=7, scale=2)

    # mark {cid} as a primary key
    Customer.pyre_primaryKey(Customer.cid)
    # and {name} as unique
    Customer.pyre_unique(Customer.name)
    # finally, attach some nameless constraints: the balance is never negative
    Customer.pyre_check(Customer.balance >= 0)
    # and stays below a limit
    Customer.pyre_check(Customer.balance < 10000)

    # declare the order table
    class Order(pyre.db.table, id="orders"):
        """
        Trivial order table
        """

        # the identifier of the order
        oid = pyre.db.int().primary()
        # and of the customer who placed it
        cid = pyre.db.int()

    # mark {cid} as a foreign key
    Order.pyre_foreignKey(field=Order.cid, foreign=Customer.cid)

    # get a server
    server = pyre.db.server(name="test")

    # generate the SQL statement that creates the customer table
    statement = tuple(server.sql.createTable(table=Customer))
    # and check it
    assert statement == (
        "CREATE TABLE customers",
        "  --",
        "  -- Simple customer table",
        "  --",
        "(",
        "  cid INTEGER, -- the customer id",
        "  name CLOB",
        "    NOT NULL,",
        "  phone VARCHAR(10),",
        "  balance DECIMAL(7, 2),",
        "",
        "  PRIMARY KEY (cid),",
        "  UNIQUE (name),",
        "  CHECK ((balance) >= (0)),",
        "  CHECK ((balance) < (10000))",
        ");",
    )

    # and the SQL statement that creates the order table
    statement = tuple(server.sql.createTable(table=Order))
    # and check it
    assert statement == (
        "CREATE TABLE orders",
        "  --",
        "  -- Trivial order table",
        "  --",
        "(",
        "  oid INTEGER",
        "    PRIMARY KEY,",
        "  cid INTEGER,",
        "",
        "  FOREIGN KEY (cid) REFERENCES customers (cid)",
        ");",
    )

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
