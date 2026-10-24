#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that the parser holds the user information and the host of an authority to RFC 3986
"""


def test() -> None:
    """
    Parse uris with valid and invalid user information and hosts
    """
    # the home of the parser
    from pyre.primitives import uri

    # a user and a password
    assert uri.parse("ftp://me:secret@host/").server == ("host", None, "me", "secret")
    # a host with the characters a registered name may hold
    assert uri.parse("s3://bucket_1.example-host~2/").server == (
        "bucket_1.example-host~2",
        None,
        None,
        None,
    )

    # each of these
    for text in ("http://a@b@host/", "http://ho st/", "http://ho<st/", "http://host^/"):
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
