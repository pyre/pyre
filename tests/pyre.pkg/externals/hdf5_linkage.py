#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
The linkage settles which mpi a flavor-ambiguous parallel hdf5 was built against

Conda and macports name every hdf5 flavor {hdf5}, and the build configuration header
proves only that a build is mpi aware, not which implementation it bound to. The library
itself names it. Here the installation is called {hdf5} and links against mpich, so the
openmpi recipe must be refused even though it is the preferred one
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
    Resolve an ambiguously named parallel hdf5 and check what the linkage decides
    """
    # the engine to fake
    from pyre.platforms.DPkg import DPkg

    # the index class
    from pyre.externals.Index import Index

    # make a scratch installation to point the fake database at
    with tempfile.TemporaryDirectory() as scratch:
        # the canonical layout
        include = os.path.join(scratch, "include")
        lib = os.path.join(scratch, "lib")
        # make the folders
        os.makedirs(include)
        os.makedirs(lib)

        # the umbrella header, which the recipe uses as its marker
        open(os.path.join(include, "hdf5.h"), "w").close()
        # the build configuration header, declaring a parallel build
        with open(os.path.join(include, "H5pubconf.h"), "w") as stream:
            # exactly as a real parallel build does
            stream.write("#define H5_HAVE_PARALLEL 1\n")
            stream.write('#define H5_VERSION "1.14.5"\n')
        # the library, linked against mpich rather than openmpi
        with open(os.path.join(lib, "libhdf5.so"), "wb") as stream:
            # mpich's runtime carries a different version than openmpi's
            stream.write(elf(needed=("libmpi.so.12", "libc.so.6")))

        # the fake database: one ambiguously named package, as conda would have it
        installed = {"hdf5": ("1.14.5", "1")}
        # whose contents are the scratch installation
        contents = {
            "hdf5": [
                os.path.join(include, "hdf5.h"),
                os.path.join(include, "H5pubconf.h"),
                os.path.join(lib, "libhdf5.so"),
            ]
        }

        # an engine wired to the fake database instead of a dpkg client
        class engine(DPkg):
            """
            A dpkg engine over canned data
            """

            # the installed package index
            def getInstalledPackages(self):
                """
                Serve the canned index
                """
                # easy enough
                return installed

            # package contents
            def retrievePackageContents(self, package):
                """
                Serve the canned contents
                """
                # easy enough
                yield from contents[package]
                # all done
                return

        # make a private index over the fake engine
        index = Index()
        # wire it
        index._engines = (engine(name="dpkg.fake.hdf5.linkage"),)
        # resolve an unconstrained request
        report = index.resolve(requested=["hdf5"])

        # the serial recipe was refuted by the header, the openmpi recipe by the library,
        # and the mpich recipe claimed the build; the name said nothing at any point
        assert report.selections["hdf5"].flavor == "hdf5-mpich"
        # it answers to the parallel class
        assert "parallel" in report.selections["hdf5"].tags
        # and to the implementation the library named
        assert "mpich" in report.selections["hdf5"].tags

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
