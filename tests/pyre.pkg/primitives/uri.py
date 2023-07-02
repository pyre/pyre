#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


"""
Exercise the uri primitive
"""


def test():
    # the home of the factory
    from pyre.primitives import uri

    # grab the parser
    p = uri.parse

    # a simple example
    url = p("https://www.example.com/")
    # check
    assert url.scheme == "https"
    assert url.authority == "www.example.com"
    assert url.address == "/"
    assert url.query is None
    assert url.fragment is None
    assert url.server == ("www.example.com", None, None, None)

    # access an s3 bucket
    url = p("s3://parasim@us-west/bucket/file.h5")
    # check
    assert url.scheme == "s3"
    assert url.authority == "parasim@us-west"
    assert url.address == "/bucket/file.h5"
    assert url.query is None
    assert url.fragment is None
    assert url.server == ("us-west", None, "parasim", None)

    # all done
    return


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    test()


# end of file
