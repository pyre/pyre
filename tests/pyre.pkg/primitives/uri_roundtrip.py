#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a uri reads back as it was written, keeping the parts that are there but empty, as
RFC 3986 asks of recomposition
"""


def test() -> None:
    """
    Parse uris with empty parts and turn them back into text
    """
    # the home of the parser
    from pyre.primitives import uri

    # each of these
    for text in (
        "file:///tmp/a",
        "a?",
        "a#",
        "a?#",
        "//host",
        "file:",
        "http://host/p?q#f",
        "http://me@[::1]:80/p",
    ):
        # reads back as it was written
        assert str(uri.parse(text)) == text, text

    # all done
    return


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    test()


# end of file
