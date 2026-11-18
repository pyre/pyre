#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that an S3 filesystem keeps a file that has the name of the folder that holds it, whether
or not the folder has an object of its own
"""


class Paginator:
    """
    List a bucket whose folders hold files named after them
    """

    # the pages of the bucket, by prefix
    pages = {
        # the root holds two folders
        "products/": {
            "CommonPrefixes": [{"Prefix": "products/V54/"}, {"Prefix": "products/V55/"}],
        },
        # a folder with its own object and a file named after it
        "products/V54/": {
            "Contents": [{"Key": "products/V54/"}, {"Key": "products/V54/V54"}],
        },
        # a folder with a file named after it, and no object of its own
        "products/V55/": {
            "Contents": [{"Key": "products/V55/V55"}],
        },
    }

    # interface
    def paginate(self, Bucket, Prefix, Delimiter):
        """
        Generate the pages of the listing of {Prefix}
        """
        # one page per prefix
        yield self.pages[Prefix]
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
        # make one
        return Paginator()


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
        return Client()


def test():
    # support
    import pyre.filesystem

    # a filesystem over a bucket
    fs = pyre.filesystem.s3(
        session=Session(), root=pyre.primitives.uri.parse("s3://bucket/products")
    )
    # list all of it
    fs.discover(levels=None)

    # each folder holds the file named after it
    for name in ("V54", "V55"):
        # by its name
        assert sorted(fs[name].contents) == [name]
        # and it is a file
        assert not fs[name][name].isFolder
    # all done
    return fs


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
