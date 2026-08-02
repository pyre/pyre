#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
The elf reader extracts the dynamic table of a synthesized image

The image is assembled here rather than committed, so the check is deterministic on any
host and the layout it depends on is written down where a reader can see it
"""

# externals
import struct


def elf(needed=(), soname=None, runpath=None):
    """
    Assemble a minimal 64-bit little endian elf image carrying the given dynamic entries
    """
    # the names the string table must hold
    names = ([soname] if soname else []) + list(needed) + ([runpath] if runpath else [])
    # build the table, which opens with the empty string
    strtab = bytearray(b"\0")
    # recording where each name lands
    offsets = {}
    # go through them
    for name in names:
        # note the offset
        offsets[name] = len(strtab)
        # and append the null terminated name
        strtab += name.encode() + b"\0"

    # the dynamic entries, as (tag, value) pairs
    entries = []
    # the image announces itself first, when it has a name
    if soname:
        # DT_SONAME
        entries.append((14, offsets[soname]))
    # then the libraries it loads
    for name in needed:
        # DT_NEEDED
        entries.append((1, offsets[name]))
    # then the search path, when there is one
    if runpath:
        # DT_RUNPATH
        entries.append((29, offsets[runpath]))

    # the header is 64 bytes and the two program headers 56 each, so the dynamic table
    # starts here
    dynoff = 64 + 2 * 56
    # it carries one entry per pair, plus the string table locator and the terminator,
    # at 16 bytes each
    dynsize = (len(entries) + 2) * 16
    # and the string table follows it
    stroff = dynoff + dynsize
    # the whole image ends there
    total = stroff + len(strtab)

    # the identification bytes: the magic, 64 bit, little endian, current version
    image = bytearray(b"\x7fELF" + bytes([2, 1, 1, 0]) + b"\0" * 8)
    # the rest of the header: a shared object for x86-64, with no section table
    image += struct.pack("<HHI", 3, 0x3E, 1)
    # the entry point, the program header offset, no section headers, no flags
    image += struct.pack("<QQQI", 0, 64, 0, 0)
    # the header sizes and counts; the section fields are all zero
    image += struct.pack("<HHHHHH", 64, 56, 2, 0, 0, 0)

    # the first program header maps the whole file at address zero, so that a load
    # address and a file offset are the same number and the reader's arithmetic shows
    image += struct.pack("<IIQQQQQQ", 1, 5, 0, 0, 0, total, total, 0x1000)
    # the second locates the dynamic table
    image += struct.pack("<IIQQQQQQ", 2, 6, dynoff, dynoff, dynoff, dynsize, dynsize, 8)

    # the dynamic entries
    for tag, value in entries:
        # each is a tag and a value
        image += struct.pack("<QQ", tag, value)
    # the table locates the strings, and is terminated
    image += struct.pack("<QQ", 5, stroff)
    # by the null tag
    image += struct.pack("<QQ", 0, 0)

    # finally the string table
    image += strtab
    # hand back the image
    return bytes(image)


def test():
    """
    Read a synthesized image and check what the reader makes of it
    """
    # support
    import pyre.platforms.binaries as binaries

    # the reader
    from pyre.platforms.binaries.ELF import ELF

    # assemble an image that loads two libraries and announces itself
    data = elf(needed=("libmpi.so.40", "libc.so.6"), soname="libhdf5.so.310", runpath="/opt/lib")
    # read it, handing over the contents directly so there is no file to make
    image = ELF(path="synthetic.so", data=data)

    # the reader must see both libraries, in the order the table lists them
    assert list(image.dependencies) == ["libmpi.so.40", "libc.so.6"]
    # the name the image announces itself by
    assert image.soname == "libhdf5.so.310"
    # and the search path baked into it
    assert list(image.searchpath) == ["/opt/lib"]
    # the dispatcher must recognize it as ours
    assert binaries.elf.claims(data)

    # an image with no dynamic entries at all
    bare = ELF(path="bare.so", data=elf())
    # names nothing
    assert list(bare.dependencies) == []
    # and announces nothing
    assert bare.soname is None

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
