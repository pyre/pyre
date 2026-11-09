#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that an S3 filesystem whose listing is refused because the credentials have expired says
so, naming the folder whose listing was interrupted
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
    Refuse every listing because the credentials have expired
    """

    # interface
    def paginate(self, Bucket, Prefix, Delimiter):
        """
        Refuse the listing of {Prefix}
        """
        # the token is no longer good
        raise ClientError(code="ExpiredToken")


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
        assert False, "the listing went through with expired credentials"
    # the refusal says the credentials have expired
    except fs.ExpiredCredentialsError as error:
        # and names the folder
        assert error.uri.authority == "bucket"
        # whose listing was refused
        assert str(error.uri.address) == "/products"
        # it remembers what S3 said
        assert isinstance(error.__cause__, ClientError)
    # all done
    return fs


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
