#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
The reader is chosen by what the file announces itself to be, and unknown files are refused
"""


def test():
    """
    Offer the readers a variety of leading bytes and check who claims what
    """
    # support
    import pyre.platforms.binaries as binaries

    # the elf identification bytes belong to the elf reader
    assert binaries.elf.claims(b"\x7fELF\x02\x01\x01\x00")
    # and to nobody else
    assert not binaries.macho.claims(b"\x7fELF\x02\x01\x01\x00")

    # the thin mach-o magics, in both widths
    assert binaries.macho.claims(b"\xcf\xfa\xed\xfe")
    assert binaries.macho.claims(b"\xce\xfa\xed\xfe")
    # the universal wrapper, which is written big endian
    assert binaries.macho.claims(b"\xca\xfe\xba\xbe")
    # none of which is an elf image
    assert not binaries.elf.claims(b"\xcf\xfa\xed\xfe")

    # a file that announces nothing belongs to nobody
    assert not binaries.elf.claims(b"#!/bin/sh\n")
    assert not binaries.macho.claims(b"#!/bin/sh\n")
    # and a file too short to carry a magic number is refused rather than crashing
    assert not binaries.macho.claims(b"\xcf\xfa")

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
