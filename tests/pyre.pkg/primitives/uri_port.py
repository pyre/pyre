#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that the parser accepts only digits as the port of an authority, and none at all
"""


def test() -> None:
    """
    Parse uris with numeric, empty and invalid ports
    """
    # the home of the parser
    from pyre.primitives import uri

    # a port is a number
    assert uri.parse("http://host:80/p").server == ("host", "80", None, None)
    # or nothing at all, as if it were not there
    assert uri.parse("http://host:/p").server == ("host", None, None, None)

    # each of these
    for text in ("http://host:x/p", "http://host:8o/p", "http://host:80:81/p"):
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
