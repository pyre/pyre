#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that internet addresses write text that reads back as the same address, for hosts and
ports as well as for unix sockets
"""


def test() -> None:
    """
    Write an ip address and a unix socket, and read them back
    """
    # support
    import pyre

    # make a schema
    schema = pyre.schemata.inet()

    # an ip address
    ip = schema.coerce(value="localhost:5000")
    # writes its host and port
    assert schema.string(ip) == "localhost:5000", schema.string(ip)
    # read back
    copy = schema.coerce(value=schema.string(ip))
    # it is the same address
    assert (copy.host, copy.port) == ("localhost", 5000), (copy.host, copy.port)

    # a unix socket
    socket = schema.coerce(value="unix:/tmp/pyre.socket")
    # writes its family and its path
    assert schema.string(socket) == "unix:/tmp/pyre.socket", schema.string(socket)
    # read back
    copy = schema.coerce(value=schema.string(socket))
    # it is a unix socket again
    assert isinstance(copy, schema.unix), copy
    # with the same path
    assert copy.path == "/tmp/pyre.socket", copy.path

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
