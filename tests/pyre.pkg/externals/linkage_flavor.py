#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
A linkage settles which implementation a library was built against

The library is synthesized and written to a scratch directory, so the check exercises the
folder scan and the image reader together, deterministically and on any host
"""

# externals
import os
import struct
import tempfile


def elf(needed=()):
    """
    Assemble a minimal 64-bit little endian elf image that loads the given libraries
    """
    # build the string table, which opens with the empty string
    strtab = bytearray(b"\0")
    # recording where each name lands
    offsets = {}
    # go through the names
    for name in needed:
        # note the offset
        offsets[name] = len(strtab)
        # and append the null terminated name
        strtab += name.encode() + b"\0"

    # one dynamic entry per library
    entries = [(1, offsets[name]) for name in needed]
    # the header is 64 bytes and the two program headers 56 each
    dynoff = 64 + 2 * 56
    # the table carries the entries, the string table locator, and the terminator
    dynsize = (len(entries) + 2) * 16
    # the string table follows
    stroff = dynoff + dynsize
    # and the image ends there
    total = stroff + len(strtab)

    # the identification bytes: the magic, 64 bit, little endian, current version
    image = bytearray(b"\x7fELF" + bytes([2, 1, 1, 0]) + b"\0" * 8)
    # a shared object for x86-64
    image += struct.pack("<HHI", 3, 0x3E, 1)
    # the entry point, the program header offset, no section headers
    image += struct.pack("<QQQI", 0, 64, 0, 0)
    # the header sizes and counts
    image += struct.pack("<HHHHHH", 64, 56, 2, 0, 0, 0)
    # the first program header maps the whole file at address zero
    image += struct.pack("<IIQQQQQQ", 1, 5, 0, 0, 0, total, total, 0x1000)
    # the second locates the dynamic table
    image += struct.pack("<IIQQQQQQ", 2, 6, dynoff, dynoff, dynoff, dynsize, dynsize, 8)
    # the entries
    for tag, value in entries:
        # one tag and value pair each
        image += struct.pack("<QQ", tag, value)
    # the string table locator
    image += struct.pack("<QQ", 5, stroff)
    # the terminator
    image += struct.pack("<QQ", 0, 0)
    # and the strings
    image += strtab
    # hand back the image
    return bytes(image)


def test():
    """
    Evaluate linkages against synthesized libraries
    """
    # support
    import pyre

    # the class under test
    from pyre.externals.Linkage import Linkage

    # the patterns the hdf5 recipes use to tell the mpi implementations apart
    openmpi = Linkage(library="hdf5", pattern=r"libmpi\.(so\.4\d|4\d\.dylib)")
    mpich = Linkage(library="hdf5", pattern=r"libmpich|libmpi\.(so\.1\d|1\d\.dylib)")

    # make a scratch directory to hold the synthesized libraries
    with tempfile.TemporaryDirectory() as scratch:
        # as a path the folder scan understands
        folder = pyre.primitives.path(scratch)
        # the folders a recipe would hand over
        folders = (folder,)

        # write an hdf5 built against openmpi
        with open(os.path.join(scratch, "libhdf5.so"), "wb") as stream:
            # naming the openmpi runtime, exactly as debian's parallel build does
            stream.write(elf(needed=("libmpi.so.40", "libc.so.6")))

        # the openmpi linkage claims it
        ok, values = openmpi.evaluate(folders=folders)
        assert ok and not values
        # and the mpich linkage refuses it
        ok, values = mpich.evaluate(folders=folders)
        assert not ok

        # replace it with a serial build, which names no mpi at all
        with open(os.path.join(scratch, "libhdf5.so"), "wb") as stream:
            # just the c runtime
            stream.write(elf(needed=("libc.so.6",)))

        # neither parallel linkage claims it
        assert not openmpi.evaluate(folders=folders)[0]
        assert not mpich.evaluate(folders=folders)[0]
        # while an exclusion is satisfied: the build links to no mpi
        forbidden = Linkage(library="hdf5", pattern=r"libmpi", forbid=True)
        assert forbidden.evaluate(folders=folders)[0]

        # and an extractor names what it found
        harvester = Linkage(library="hdf5", pattern=r"(libc\.so\.\d+)", harvest="version")
        ok, values = harvester.evaluate(folders=folders)
        assert ok and values == {"version": "libc.so.6"}

    # with the scratch directory gone, the library is nowhere to be found, so every
    # linkage abstains: nothing readable means no evidence either way, and a check that
    # vetoed on silence would reject installations their headers already proved good
    assert openmpi.evaluate(folders=folders) == (True, {})
    assert mpich.evaluate(folders=folders) == (True, {})
    assert Linkage(library="hdf5", pattern=r"libmpi", forbid=True).evaluate(folders=folders)[0]
    assert harvester.evaluate(folders=folders) == (True, {})

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
