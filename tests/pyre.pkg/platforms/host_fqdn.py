#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that the fully qualified domain name of the host is resolved on first use and once: the
reverse lookup can block for the resolver timeout, and most processes never need it
"""

# support
import pyre


def test():
    # the resolver
    import socket

    # get the host, and the platform class that holds the resolved name
    host = pyre.executive.host
    platform = type(host)
    # forget whatever the boot may have resolved: a configured host map is allowed to ask
    platform._fqdn = None
    # count the calls to the resolver
    calls = []
    # by wrapping it
    resolve = socket.getfqdn
    socket.getfqdn = lambda *args, **kwds: calls.append(1) or resolve(*args, **kwds)
    # carefully
    try:
        # nothing has been resolved yet
        assert platform._fqdn is None
        assert calls == []
        # asking for the name resolves it
        fqdn = host.fqdn
        assert isinstance(fqdn, str)
        assert calls == [1]
        # asking again does not
        assert host.fqdn is fqdn
        assert calls == [1]
        # and the platform class answers the same, without asking either
        assert platform.fqdn is fqdn
        assert calls == [1]
    # restore the resolver
    finally:
        socket.getfqdn = resolve
    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
