#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that the parser refuses a fragment that holds another fragment marker
"""


def test() -> None:
    """
    Parse uris with valid and invalid fragments
    """
    # the home of the parser
    from pyre.primitives import uri

    # a fragment on its own
    assert uri.parse("#name").fragment == "name"
    # a fragment may hold slashes and question marks
    assert uri.parse("a#b/c?d").fragment == "b/c?d"

    # each of these
    for text in ("a#b#c", "#b#"):
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
