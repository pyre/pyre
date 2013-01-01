#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


"""
Instantiate the sqlite component
"""


def test():
    # access the package
    import pyre.db

    # build a database component
    db = pyre.db.sqlite()

    # and return it
    return db


# main
if __name__ == "__main__":
    test()


# end of file 
