#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a field hands over its value as the octets the server sent, before any decoding
"""


def test():
    """
    Read a text value, an octet string and a null through the raw octets of their fields
    """
    # access the bindings
    from pyre.extensions import libpq

    # open a session
    connection = libpq.Connection({"dbname": "postgres"})
    # select a text value with a character beyond ascii, an octet string, and nothing
    result = connection.exec("SELECT 'héllo'::text, '\\x00ff'::bytea, NULL::text")
    # get the row
    row = result[0]
    # the text arrives in the encoding of the session
    assert row.field(0).bytes == "héllo".encode("utf-8"), row.field(0).bytes
    # the octet string arrives escaped, as the server writes it in text
    assert row.field(1).bytes == b"\\x00ff", row.field(1).bytes
    # and a value that is not there has no octets
    assert row.field(2).bytes is None, row.field(2).bytes
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
