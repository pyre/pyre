#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that the web shell's service specification is configurable and resolves through the
nexus service slot the way {launch} wires it
"""


def test():
    # get access to the framework
    import pyre

    # get the web shell
    from pyre.shells.Web import Web

    # instantiate one
    shell = Web(name="test.shells.web")
    # out of the box, it fields requests with the stock http server
    assert shell.service == "http"

    # a hosting application can point the shell at its own flavor; this import spec stands in
    # for one, resolving to the stock server through a different route
    shell.service = "import:pyre.http.Server.Server"

    # mirror the wiring in {launch}: build a nexus
    nexus = pyre.nexus.node(name="test.shells.web.nexus")
    # and register the web service using the shell's specification
    nexus.services["web"] = shell.service
    # the slot resolves the spec into a live component
    web = nexus.services["web"]
    # of the expected pedigree
    assert web.pyre_family() == "pyre.nexus.servers.http"
    # named within the nexus namespace, so its configuration, e.g. the address, lives at the
    # conventional location
    assert web.pyre_name == "test.shells.web.nexus.services.web"

    # all done
    return shell


# main
if __name__ == "__main__":
    test()


# end of file
