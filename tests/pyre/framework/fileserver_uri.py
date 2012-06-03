#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


"""
Exercise file opening by the file server
"""


def test():
    import os
    import pyre.framework
    f = pyre.framework.executive(managers=pyre.framework).fileserver

    # a simple case that looks for a file in the current directory
    encoding, stream = f.open(scheme="file", address="sample.odb")
    assert encoding == 'odb'
    assert stream.name == 'sample.odb'

    # using absolute path for the same file
    encoding, stream = f.open(scheme='file', address=os.path.abspath("sample.odb"))
    assert encoding == 'odb'
    assert stream.name == os.path.abspath('sample.odb')

    # using vfs
    encoding, stream = f.open(scheme="vfs", address="/local/sample.odb")
    assert encoding == 'odb'
    assert stream.name == os.path.abspath('sample.odb')

    # test failure modes
    # bad scheme
    try:
        f.open(scheme="unknown", address="sample.odb")
        assert False
    except f.URISpecificationError as error:
        assert error.uri == "unknown://sample.odb"
        assert error.reason == "unsupported scheme 'unknown'"

    # missing physical file 
    try:
        f.open(scheme="file", address="not-there.odb")
        assert False
    except f.NotFoundError as error:
        assert error.filesystem == f
        assert error.uri == 'not-there.odb'
        assert error.fragment == 'file'

    # missing logical file
    try:
        f.open(scheme='vfs', address='/local/not-there.odb')
        assert False
    except f.NotFoundError as error:
        assert error.filesystem == f
        assert error.uri == '/local/not-there.odb'
        assert error.fragment == 'not-there.odb'

    # missing logical directory
    try:
        f.open(scheme='vfs', address='/oops/not-there.odb')
        assert False
    except f.NotFoundError as error:
        assert error.filesystem == f
        assert error.uri == '/oops/not-there.odb'
        assert error.fragment == 'oops'

    # return the file server
    return f


# main
if __name__ == "__main__":
    test()


# end of file 
