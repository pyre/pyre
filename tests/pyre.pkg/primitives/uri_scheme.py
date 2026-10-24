#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that the parser holds a scheme to the syntax of RFC 3986
"""


def test() -> None:
    """
    Parse uris with valid and invalid schemes
    """
    # the home of the parser
    from pyre.primitives import uri

    # a scheme starts with a letter, and may hold letters, digits, plus, minus and dot
    assert uri.parse("svn+ssh.v-2://host/repo").scheme == "svn+ssh.v-2"

    # each of these
    for text in ("1x://a", "+a:b", ".a:b", "my file:v2.txt", ":a"):
        # attempt to
        try:
            # parse it
            uri.parse(text)
            # which should be unreachable
            assert False, text
        # if it is refused, as expected
        except uri.ParsingError:
            # all good
            pass

    # all done
    return


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    test()


# end of file
