#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a process forked after an S3 filesystem made its client gets a client of its own,
since connections cannot be shared across a fork
"""

# externals
import os


class Session:
    """
    Make clients
    """

    # interface
    def client(self, service):
        """
        Make a client for {service}
        """
        # make one
        return object()


def test():
    # support
    import pyre.filesystem

    # a filesystem over a bucket
    fs = pyre.filesystem.s3(
        session=Session(), root=pyre.primitives.uri.parse("s3://bucket/products")
    )
    # get its client
    client = fs.client
    # fork
    pid = os.fork()
    # in the child
    if pid == 0:
        # the client is a new one, and it is kept from then on
        mine = fs.client is not client and fs.client is fs.client
        # report by the exit status, without running the parent's exit handlers
        os._exit(0 if mine else 1)
    # in the parent, wait for the child
    _, status = os.waitpid(pid, 0)
    # it must have found a client of its own
    assert os.waitstatus_to_exitcode(status) == 0
    # while the parent kept the original
    assert fs.client is client
    # all done
    return fs


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
