#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that an S3 filesystem can tell whether the credentials of its session have expired, and
that a key that isn't there is not taken for expired credentials
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


class Client:
    """
    Answer requests for the bytes of a key with a fixed refusal, or with the bytes
    """

    # the exceptions i raise
    exceptions = Exceptions

    # metamethods
    def __init__(self, code, **kwds):
        # chain up
        super().__init__(**kwds)
        # the reason i refuse requests, if any
        self.code = code
        # all done
        return

    # interface
    def get_object(self, Bucket, Key, Range):
        """
        Answer a request for the bytes {Range} of {Key}
        """
        # if i refuse requests
        if self.code is not None:
            # do so
            raise ClientError(code=self.code)
        # otherwise, hand back the bytes
        return {"Body": b"\x89"}


class Session:
    """
    Make clients that answer the same way
    """

    # metamethods
    def __init__(self, code, **kwds):
        # chain up
        super().__init__(**kwds)
        # the reason my clients refuse requests, if any
        self.code = code
        # all done
        return

    # interface
    def client(self, service):
        """
        Make a client for {service}
        """
        # make one
        return Client(code=self.code)


def expired(code):
    """
    Ask a filesystem whose session answers with {code} whether its credentials have expired
    """
    # support
    import pyre.filesystem

    # a filesystem over a bucket
    fs = pyre.filesystem.s3(
        session=Session(code=code), root=pyre.primitives.uri.parse("s3://bucket/products")
    )
    # ask it
    return fs.expired()


def test():
    # credentials that S3 calls expired have expired
    assert expired(code="ExpiredToken") is True
    # a key that isn't there says nothing against the credentials
    assert expired(code="NoSuchKey") is False
    # and neither does a request that succeeds
    assert expired(code=None) is False
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
