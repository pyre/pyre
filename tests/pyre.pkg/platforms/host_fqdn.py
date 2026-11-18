#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
import pyre


def test():
    """
    Check that the fully qualified domain name of the host is resolved on first use and once: the
    reverse lookup can block for the resolver timeout, and most processes never need it
    """
    # the resolver
    import socket

    # get the host
    host = pyre.executive.host
    # and the platform class that holds the resolved name
    platform = type(host)
    # forget whatever the boot may have resolved: a configured host map is allowed to ask
    platform._fqdn = None
    # count the calls to the resolver
    calls = []
    # by holding on to it
    resolve = socket.getfqdn
    # and installing a stand-in that counts before it resolves
    socket.getfqdn = lambda *args, **kwds: calls.append(1) or resolve(*args, **kwds)
    # carefully
    try:
        # nothing has been resolved yet
        assert platform._fqdn is None
        # and the resolver was not asked
        assert calls == []
        # asking for the name resolves it
        fqdn = host.fqdn
        # into a string
        assert isinstance(fqdn, str)
        # by asking the resolver once
        assert calls == [1]
        # asking again does not
        assert host.fqdn is fqdn
        # so the resolver was not asked again
        assert calls == [1]
        # and the platform class answers the same, without asking either
        assert platform.fqdn is fqdn
        # so the resolver is still at one call
        assert calls == [1]
    # restore the resolver
    finally:
        # by putting the original back
        socket.getfqdn = resolve
    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
