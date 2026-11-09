#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that an S3 filesystem whose listing is refused for a reason other than expired credentials
passes the refusal on as it is
"""


class ClientError(Exception):
    """
    A refusal by S3, with the reason it gives
    """

    # metamethods
    def __init__(self, code, **kwds):
        # chain up
        super().__init__(**kwds)
        # record the answer the way S3 shapes it
        self.response = {"Error": {"Code": code}}
        # all done
        return


class Exceptions:
    """
    The exceptions a client raises
    """

    # the refusals
    ClientError = ClientError


class Paginator:
    """
    Refuse every listing because access is denied
    """

    # interface
    def paginate(self, Bucket, Prefix, Delimiter):
        """
        Refuse the listing of {Prefix}
        """
        # the credentials don't reach the bucket
        raise ClientError(code="AccessDenied")


class Client:
    """
    Hand out paginators
    """

    # the exceptions i raise
    exceptions = Exceptions

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
    # list it
    try:
        fs.discover(levels=1)
        # which can't succeed
        assert False, "the listing went through a denial"
    # the credentials are not the problem
    except fs.ExpiredCredentialsError:
        assert False, "a denial was taken for expired credentials"
    # the refusal arrives as S3 made it
    except ClientError as error:
        # with its reason
        assert error.response["Error"]["Code"] == "AccessDenied"
    # all done
    return fs


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
