#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that a process that has imported the recruiter that forks never consults the macOS
system configuration for proxies, no matter who captured the lookup functions or when, and that
proxies named in the environment are still honored

The system configuration lookup brings CoreFoundation to life, which does not survive a fork
that is not followed by an exec; a crew member forked from such a process dies the first time
anything in it reaches CoreFoundation
"""

# externals
import os
import sys


def test():
    # this is a problem of one platform
    if sys.platform != "darwin":
        # so there is nothing to check anywhere else
        return

    # capture the lookup functions first, the way an http client does when it is imported,
    # before the recruiter has had a chance to do anything
    import urllib.request
    from urllib.request import getproxies, proxy_bypass

    # clear the environment of proxy settings, so the lookups have to go past it
    for name in list(os.environ):
        # anything that names a proxy
        if name.lower().endswith("_proxy"):
            # goes
            del os.environ[name]

    # now bring in the recruiter
    import pyre.nexus.Fork

    # the system configuration has nothing to say
    assert urllib.request.getproxies_macosx_sysconf() == {}
    # through the functions captured early as well
    assert getproxies() == {}
    # and no host bypasses anything
    assert not proxy_bypass("s3.us-west-2.amazonaws.com")
    # the names that reach the system configuration are no longer the builtins that do
    import _scproxy

    assert urllib.request._get_proxies is not _scproxy._get_proxies
    assert urllib.request._get_proxy_settings is not _scproxy._get_proxy_settings

    # a proxy named in the environment is still honored
    os.environ["https_proxy"] = "http://proxy.example.com:3128"
    assert getproxies() == {"https": "http://proxy.example.com:3128"}
    # and so is the list of hosts that bypass it
    os.environ["no_proxy"] = "amazonaws.com"
    assert proxy_bypass("s3.us-west-2.amazonaws.com")
    assert not proxy_bypass("example.org")

    # all done
    return


# main
if __name__ == "__main__":
    test()


# end of file
