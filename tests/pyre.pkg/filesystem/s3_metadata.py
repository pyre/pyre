#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that an S3 filesystem keeps what the listing of a bucket reports about each object: its
size, when it was last written, its entity tag and its storage class; a field the listing leaves
out stays unset
"""

# externals
import datetime

# when the objects were written
written = datetime.datetime(2026, 7, 16, 12, 0, tzinfo=datetime.timezone.utc)


class Paginator:
    """
    List a bucket with a file, and a folder that holds a file
    """

    # the pages of the bucket, by prefix
    pages = {
        # the root holds a file and a folder
        "products/": {
            "Contents": [
                {
                    "Key": "products/readme.txt",
                    "Size": 1024,
                    "LastModified": written,
                    "ETag": '"9e107d9d372bb6826bd81d3542a419d6"',
                    "StorageClass": "STANDARD",
                }
            ],
            "CommonPrefixes": [{"Prefix": "products/V54/"}],
        },
        # the folder holds a file written in parts, listed by a store that reports no class
        "products/V54/": {
            "Contents": [
                {
                    "Key": "products/V54/table.xlsx",
                    "Size": 0,
                    "LastModified": written,
                    "ETag": '"d41d8cd98f00b204e9800998ecf8427e-2"',
                }
            ],
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

    # get what the filesystem knows about the file at the root
    readme = fs.info(node=fs["readme.txt"])
    # its size
    assert readme.size == 1024
    # when it was written
    assert readme.modified == written
    # its entity tag, as S3 quotes it
    assert readme.etag == '"9e107d9d372bb6826bd81d3542a419d6"'
    # and its storage class
    assert readme.storageClass == "STANDARD"
    # it is still known by its place in the filesystem
    assert str(readme.uri.address) == "/products/readme.txt"

    # get what the filesystem knows about the file in the folder
    table = fs.info(node=fs["V54/table.xlsx"])
    # an empty object has a size
    assert table.size == 0
    # an object written in parts has the tag S3 gives it
    assert table.etag == '"d41d8cd98f00b204e9800998ecf8427e-2"'
    # and a field missing from the listing is unset
    assert table.storageClass is None
    # the folder itself is still a folder
    assert fs["V54"].isFolder
    # all done
    return fs


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
