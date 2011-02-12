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
    # access the package
    import pyre.postgres

    # build a database component
    db = pyre.postgres.database(name="sample")

    # and return it
    return db


# main
if __name__ == "__main__":
    test()


# end of file 
