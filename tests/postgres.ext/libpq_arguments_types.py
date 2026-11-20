#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that python lists, dictionaries and byte buffers travel as arguments of the matching
postgres types
"""


def test():
    """
    Send a list, a dictionary and the three kinds of byte buffers, and read each back
    """
    # access the bindings
    from pyre.extensions import libpq

    # open a session
    connection = libpq.Connection({"dbname": "postgres"})
    # a list of words, with the awkward ones among them
    words = ["a,b", 'say "hi"', "{x}", "", None]
    # becomes an array
    echo = connection.execute("SELECT $1::text[] AS words", words)[0]["words"]
    # and comes back intact
    assert echo == words, repr(echo)
    # a dictionary
    document = {"a": [1, 2.5, None, True], "b": "it's"}
    # becomes a json document
    echo = connection.execute("SELECT $1::jsonb AS document", document)[0]["document"]
    # and comes back intact
    assert echo == document, repr(echo)
    # and every kind of byte buffer becomes a binary string
    for buffer in [b"\x00\xffA", bytearray(b"\x00\xffA"), memoryview(b"\x00\xffA")]:
        # send it
        echo = connection.execute("SELECT $1::bytea AS octets", buffer)[0]["octets"]
        # and check it came back intact
        assert echo == b"\x00\xffA", f"{type(buffer).__name__}: {echo!r}"
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
