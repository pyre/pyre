#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that an S3 filesystem takes the object whose key is the prefix of a folder, such as the
empty object the S3 console makes for a new folder, as standing for the folder rather than as
one of its files
"""


class Paginator:
    """
    List a bucket whose folders have objects of their own
    """

    # the pages of the bucket, by prefix
    pages = {
        # the root holds its own object, a file, and two folders
        "products/": {
            "Contents": [{"Key": "products/"}, {"Key": "products/readme.txt"}],
            "CommonPrefixes": [{"Prefix": "products/V54/"}, {"Prefix": "products/V55/"}],
        },
        # a folder with its own object and a file
        "products/V54/": {
            "Contents": [{"Key": "products/V54/"}, {"Key": "products/V54/table.xlsx"}],
        },
        # a folder with nothing but its own object
        "products/V55/": {
            "Contents": [{"Key": "products/V55/"}],
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

    # the root holds the file and the two folders, and nothing named after itself
    assert sorted(fs.contents) == ["V54", "V55", "readme.txt"]
    # the folders are folders
    assert fs["V54"].isFolder and fs["V55"].isFolder
    # the first one holds its file only
    assert sorted(fs["V54"].contents) == ["table.xlsx"]
    # and the second one is empty
    assert sorted(fs["V55"].contents) == []
    # all done
    return fs


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
