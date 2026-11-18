#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test():
    """
    Exercise file opening by the file server
    """
    # externals
    import os

    # the framework
    import pyre

    # get the file server
    f = pyre.executive.fileserver

    # a simple case that looks for a file in the current directory
    stream = f.open("file:sample.odb")
    # finds it
    assert stream.name == "sample.odb"

    # using absolute path for the same file
    stream = f.open(f"file:{os.path.abspath('sample.odb')}")
    # finds it too
    assert stream.name == os.path.abspath("sample.odb")

    # and so does reaching it through the virtual filesystem
    stream = f.open(f"vfs:{f.STARTUP_DIR}/sample.odb")
    # which leads to the same file
    assert stream.name == os.path.abspath("sample.odb")

    # now the failure modes: a scheme the server does not know
    try:
        # must be refused
        f.open("unknown:sample.odb")
        # so this is unreachable
        assert False
    # and when it is
    except f.URISpecificationError as error:
        # the error names the uri
        assert error.uri.uri == "unknown:sample.odb"
        # and the reason
        assert error.reason == "unsupported scheme 'unknown'"

    # a missing physical file
    try:
        # can't be opened
        f.open("file:not-there.odb")
        # so this is unreachable
        assert False
    # and when it fails
    except f.SourceNotFoundError as error:
        # the error names the filesystem
        assert error.filesystem == f
        # and the uri
        assert error.uri.uri == "file:not-there.odb"

    # a missing logical file
    try:
        # can't be opened
        f.open(f"vfs:/{f.STARTUP_DIR}/not-there.odb")
        # so this is unreachable
        assert False
    # and when it fails
    except f.SourceNotFoundError as error:
        # the error names the filesystem
        assert error.filesystem == f
        # and the uri
        assert error.uri.uri == f"vfs:/{f.STARTUP_DIR}/not-there.odb"

    # a missing logical directory
    try:
        # can't be opened
        f.open("vfs:/oops/not-there.odb")
        # so this is unreachable
        assert False
    # and when it fails
    except f.SourceNotFoundError as error:
        # the error names the filesystem
        assert error.filesystem == f
        # and the uri
        assert error.uri.uri == "vfs:/oops/not-there.odb"

    # return the file server
    return f


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
