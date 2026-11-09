#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that an S3 filesystem makes one client from its session and lists every folder with it
"""


class Paginator:
    """
    Answer a listing with the folders a bucket holds under each prefix
    """

    # the folders under each prefix
    folders = {"products/": ["2026/"], "products/2026/": ["01/", "02/"]}

    # interface
    def paginate(self, Bucket, Prefix, Delimiter):
        """
        Generate the one page of the listing of {Prefix}
        """
        # the folders under it, spelled as the bucket spells them
        prefixes = [{"Prefix": Prefix + name} for name in self.folders.get(Prefix, [])]
        # make a page
        yield {"CommonPrefixes": prefixes}
        # all done
        return


class Client:
    """
    Hand out paginators
    """

    # interface
    def get_paginator(self, operation):
        """
        Make a paginator for {operation}
        """
        # only listings are expected
        assert operation == "list_objects_v2"
        # make one
        return Paginator()


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
        # only S3 is expected
        assert service == "s3"
        # count it
        self.clients += 1
        # and make it
        return Client()


def test():
    # support
    import pyre.filesystem

    # a session
    session = Session()
    # and a filesystem over a bucket
    fs = pyre.filesystem.s3(session=session, root=pyre.primitives.uri.parse("s3://bucket/products"))
    # no client is made before it is needed
    assert session.clients == 0
    # list the top
    fs.discover(levels=1)
    # and then a folder below it, as a walk does
    fs["2026"].discover(levels=1)
    # both listings worked
    assert sorted(fs["2026"].contents) == ["01", "02"]
    # through one client
    assert session.clients == 1
    # which the filesystem keeps
    assert fs.client is fs.client
    # all done
    return fs


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
