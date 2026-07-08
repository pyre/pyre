#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Instantiate the postgres component
"""


def test():
    # access the package
    import pyre.db

    # build a database component
    db = pyre.db.postgres()

    # and return it
    return db


# main
if __name__ == "__main__":
    test()


# end of file
