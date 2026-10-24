#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that the parser refuses control characters anywhere in a uri, while keeping blanks, which
are part of the names of the resources users type
"""


def test() -> None:
    """
    Parse uris with blanks and with control characters
    """
    # the home of the parser
    from pyre.primitives import uri

    # blanks are kept
    assert uri.parse("/tmp/my file.h5").address == "/tmp/my file.h5"

    # each of these
    for text in ("/tmp/a\nb", "/tmp/a\tb", "file:/a\x00b", "/a?q=\x7f", "/a#\x1b"):
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
