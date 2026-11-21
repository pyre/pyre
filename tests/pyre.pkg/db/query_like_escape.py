#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that a {LIKE} names its escape character, so an escaped wildcard means the same thing on
every back end
"""


def test():
    """
    Render a query whose restriction matches a pattern with an escaped wildcard
    """
    # access the package
    import pyre.db

    # a table of offers
    class Offer(pyre.db.table, id="offers"):
        """
        Offers
        """

        # the description
        text = pyre.db.str()

    # the offers of fifty percent off
    class Half(pyre.db.query, offer=Offer):
        """
        The offers of fifty percent off
        """

        # the field
        text = offer.text
        # the restriction: a literal percent sign, followed by anything
        where = pyre.db.like(offer.text, "50\\%%")

    # get a server
    server = pyre.db.server()
    # generate the statement
    statement = tuple(server.sql.select(Half))
    # the restriction is the last line, and it names the escape character
    assert statement[-1] == "    ((offer.text LIKE '50\\%%' ESCAPE '\\'));", statement[-1]
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
