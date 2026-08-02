#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Each platform names the reader for the images it loads, so knowing the host settles the
format without having to guess at it
"""


def test():
    """
    Check the association between the platforms and the image readers
    """
    # support
    import pyre

    # the platforms
    from pyre.platforms.Host import Host
    from pyre.platforms.Darwin import Darwin
    from pyre.platforms.Linux import Linux

    # the readers
    from pyre.platforms.binaries.MachO import MachO
    from pyre.platforms.binaries.ELF import ELF

    # darwin loads mach-o images
    assert Darwin.image is MachO
    # linux loads elf images
    assert Linux.image is ELF
    # and a host we know nothing about promises nothing
    assert Host.image is None

    # every linux distribution inherits the association
    from pyre.platforms.Ubuntu import Ubuntu
    from pyre.platforms.Fedora import Fedora

    # so they all read elf
    assert Ubuntu.image is ELF
    assert Fedora.image is ELF

    # the running host names a reader whenever we recognize the platform
    host = pyre.executive.host
    # so check it against what the platform says it is
    if host.platform == "darwin":
        # a mac reads mach-o
        assert host.image is MachO
    elif host.platform == "linux":
        # a linux box reads elf
        assert host.image is ELF

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
