#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that the parser recognizes hosts that are IP literals, as RFC 3986 spells them
"""


def test() -> None:
    """
    Parse uris whose hosts are IPv6 addresses and future IP literals
    """
    # the home of the parser
    from pyre.primitives import uri

    # an IPv6 address, with a port
    assert uri.parse("http://[::1]:80/p").server == ("::1", "80", None, None)
    # with user information
    assert uri.parse("ftp://me@[fe80::1]/").server == ("fe80::1", None, "me", None)
    # an IPv6 address that ends in an IPv4 one
    assert uri.parse("http://[::ffff:10.0.0.1]/").server == ("::ffff:10.0.0.1", None, None, None)
    # a future IP literal
    assert uri.parse("http://[v7.a:b]/").server == ("v7.a:b", None, None, None)

    # each of these
    for text in ("http://[::1/p", "http://[zz::1]/p", "http://::1/p", "http://[v7]/"):
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
