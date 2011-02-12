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
    # access the postgres package
    import pyre.postgres

    # build a database component
    db = pyre.postgres.database(name="postgres-attach")
    # connect to the database specified in the local configuration file
    db.attach()

    # and return the component
    return db


# main
if __name__ == "__main__":
    test()


# end of file 
