#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that an S3 filesystem handed a new session makes its next client from it
"""


class Session:
    """
    Make clients, and count them
    """

    # metamethods
    def __init__(self, **kwds):
        # chain up
        super().__init__(**kwds)
        # no clients yet
        self.clients = 0
        # all done
        return

    # interface
    def client(self, service):
        """
        Make a client for {service}
        """
        # count it
        self.clients += 1
        # and make it
        return object()


def test():
    # support
    import pyre.filesystem

    # a session
    old = Session()
    # and a filesystem over a bucket
    fs = pyre.filesystem.s3(session=old, root=pyre.primitives.uri.parse("s3://bucket/products"))
    # get its client
    client = fs.client
    # hand it a new session, e.g. one with renewed credentials
    new = Session()
    fs.session = new
    # the filesystem now speaks through it
    assert fs.session is new
    # with a client of its own
    assert fs.client is not client
    # made by the new session
    assert new.clients == 1
    # and not by the old one again
    assert old.clients == 1
    # all done
    return fs


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
