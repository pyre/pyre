# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Readers for the loadable binary images of the supported platforms

The readers parse the container structure and hand it over, so that extracting a field
none of them names is a matter of reading the parsed table rather than teaching them a
new trick. They are pure python: nothing here shells out to {otool} or {readelf}, so the
same code answers in a container, over a mount, and on a host with no toolchain at all

They live here because each format belongs to a platform, which is where the rest of
that knowledge is kept; the association is in the platform classes, so that knowing the
host settles the format. Nothing here depends on the host it runs on, though: a reader
interprets what a file says it is, so a mac reads elf images and a linux box reads
mach-o ones, which is how the tests exercise both formats everywhere
"""

# the exceptions
from . import exceptions

# the readers
from .Image import Image as image
from .MachO import MachO as macho
from .ELF import ELF as elf


# the readers, in the order they are offered a file
readers = (macho, elf)


# access to the images on this host
def read(path, **kwds):
    """
    Read the binary image at {path} with whichever reader recognizes it
    """
    # pull enough of the file to identify it; every format we know announces itself in
    # its first few bytes
    with open(str(path), "rb") as stream:
        # a magic number is never longer than this
        leading = stream.read(16)
    # go through the readers
    for reader in readers:
        # offering each one the chance to claim the file
        if reader.claims(leading):
            # and handing the job to the first that does
            return reader(path=path, **kwds)
    # nothing recognized the file
    raise exceptions.FormatError(path=path, problem="unrecognized image format")


# end of file
