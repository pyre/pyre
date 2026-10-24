#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that the parser spells schemes in lower case, which is their canonical form in RFC 3986
"""


def test() -> None:
    """
    Parse uris whose schemes are not in lower case
    """
    # the home of the parser
    from pyre.primitives import uri

    # a scheme in upper case
    assert uri.parse("FILE:/tmp/a").scheme == "file"
    # one in mixed case
    assert uri.parse("Https://host/p").scheme == "https"
    # the rest of the uri is left as it was typed
    assert str(uri.parse("HTTP://Host/Path")) == "http://Host/Path"

    # all done
    return


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    test()


# end of file
