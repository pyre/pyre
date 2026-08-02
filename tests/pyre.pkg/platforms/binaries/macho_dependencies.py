#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
The mach-o reader walks the load commands of a synthesized image

The image is assembled here rather than committed, so the check is deterministic on any
host and the layout it depends on is written down where a reader can see it
"""

# externals
import struct


def command(tag, name):
    """
    Assemble a load command of kind {tag} that carries the library {name}
    """
    # the name is stored after the six fields of the command
    offset = 24
    # the payload is the null terminated name, padded so the command ends on an eight
    # byte boundary
    payload = name.encode() + b"\0"
    # work out the padding
    padding = -(offset + len(payload)) % 8
    # the total extent of the command
    size = offset + len(payload) + padding
    # the fields: the tag, the extent, where the name sits, and three version words
    body = struct.pack("<6I", tag, size, offset, 0, 0, 0)
    # followed by the name and its padding
    return body + payload + b"\0" * padding


def macho(loads=(), identity=None):
    """
    Assemble a minimal 64-bit little endian mach-o image with the given load commands
    """
    # the commands: the identity first, when there is one
    commands = [command(0x0D, identity)] if identity else []
    # then one per library the image loads
    commands += [command(0x0C, name) for name in loads]
    # splice them together
    table = b"".join(commands)

    # the header: the 64 bit magic, an arm64 dynamic library
    header = struct.pack("<8I", 0xFEEDFACF, 0x0100000C, 0, 6, len(commands), len(table), 0, 0)
    # hand back the image
    return header + table


def test():
    """
    Read a synthesized image and check what the reader makes of it
    """
    # support
    import pyre.platforms.binaries as binaries

    # the reader
    from pyre.platforms.binaries.MachO import MachO

    # assemble an image that loads two libraries and announces itself
    data = macho(
        loads=("@rpath/libmpi.40.dylib", "/usr/lib/libSystem.B.dylib"),
        identity="@rpath/libhdf5.310.dylib",
    )
    # read it, handing over the contents directly so there is no file to make
    image = MachO(path="synthetic.dylib", data=data)

    # the reader must see both libraries, in the order the table lists them
    assert list(image.dependencies) == [
        "@rpath/libmpi.40.dylib",
        "/usr/lib/libSystem.B.dylib",
    ]
    # the install name the image announces itself by
    assert image.soname == "@rpath/libhdf5.310.dylib"
    # the dispatcher must recognize it as ours
    assert binaries.macho.claims(data)

    # an image with no load commands at all
    bare = MachO(path="bare.dylib", data=macho())
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
