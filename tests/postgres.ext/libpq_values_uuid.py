#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that universally unique identifiers reach python as {uuid.UUID}
"""


def test():
    """
    Read a {uuid} value through the bindings
    """
    # support
    import uuid

    # access the bindings
    from pyre.extensions import libpq

    # open a session
    connection = libpq.Connection({"dbname": "postgres"})
    # ask for an identifier
    value = connection.exec("SELECT 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11'::uuid AS id")[0]["id"]
    # it is the identifier python would make out of the same text
    assert value == uuid.UUID("a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11"), repr(value)
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
