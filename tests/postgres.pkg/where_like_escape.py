#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that an escaped wildcard in a pattern matches only itself
"""


def test():
    """
    Select the offers of fifty percent off, and none of the offers of five hundred
    """
    # access the package
    import pyre.db

    # a table of offers
    class Offer(pyre.db.table, id="pyre_where_like_escape"):
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

    # connect
    db = pyre.db.postgres(name="queries").attach()
    # in a transaction that leaves nothing behind
    db.execute("BEGIN")
    # carefully
    try:
        # make the table
        db.createTable(Offer)
        # with a few offers
        db.execute(
            "INSERT INTO pyre_where_like_escape (text) VALUES ('50% off'), ('500 off'), ('5000')"
        )
        # only the one with the percent sign qualifies
        found = [row.text for row in db.select(Half)]
        # so check
        assert found == ["50% off"], found
    # either way
    finally:
        # leave nothing behind
        db.execute("ROLLBACK")
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
