#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test():
    """
    Sanity check: verify that the transport protocol resolves its implementations
    """
    # get the package
    import pyre.ipc

    # the default transport is the pipe flavor
    assert pyre.ipc.transport.pyre_default() is pyre.ipc.pipe()
    # the foundries resolve to the expected components: the pipe one
    assert pyre.ipc.pipe().pyre_family() == "pyre.ipc.transports.pipe"
    # the socket one
    assert pyre.ipc.socket().pyre_family() == "pyre.ipc.transports.socket"
    # user configuration specs resolve through the protocol: the pipe one
    assert pyre.ipc.transport.pyre_resolveSpecification(spec="pipe") is pyre.ipc.pipe()
    # and the socket one
    assert pyre.ipc.transport.pyre_resolveSpecification(spec="socket") is pyre.ipc.socket()

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
