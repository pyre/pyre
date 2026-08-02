# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# superclass
from .Image import Image


# the reader of mach-o images
class MachO(Image):
    """
    A reader of the mach-o images used by macOS

    The format is a header followed by a table of variable length load commands, each
    tagged with its kind. {commands} walks that table and hands over every entry, so
    mining a command this class doesn't interpret means matching on its tag rather than
    parsing the container again. Universal files carry several images at once; this
    reader selects one slice and reads it as if it were alone in the file
    """

    # constants
    # the magic numbers of thin images, in both byte orders
    magic32 = 0xFEEDFACE
    magic64 = 0xFEEDFACF
    cigam32 = 0xCEFAEDFE
    cigam64 = 0xCFFAEDFE
    # and of universal files, which are always big endian on disk
    fat = 0xCAFEBABE
    fatSwapped = 0xBEBAFECA

    # the load commands that name a shared library the image loads
    imports = frozenset(
        (
            0x0C,  # LC_LOAD_DYLIB
            0x18,  # LC_LOAD_WEAK_DYLIB
            0x1F,  # LC_REEXPORT_DYLIB
            0x20,  # LC_LAZY_LOAD_DYLIB
        )
    )
    # the load command that carries the name the image announces itself by
    identity = 0x0D  # LC_ID_DYLIB
    # the high bit that marks a command the dynamic linker must understand; it is not
    # part of the tag, so it comes off before any comparison
    required = 0x80000000

    # class interface
    @classmethod
    def claims(cls, data):
        """
        Check whether {data} opens with a magic number this reader understands
        """
        # anything shorter than a magic number
        if len(data) < 4:
            # cannot be one of ours
            return False
        # read the leading word in both byte orders
        little = int.from_bytes(data[:4], "little")
        big = int.from_bytes(data[:4], "big")
        # the thin magics, plus the universal wrapper
        known = {cls.magic32, cls.magic64, cls.cigam32, cls.cigam64, cls.fat, cls.fatSwapped}
        # claim the file if either reading lands on one of them
        return little in known or big in known

    # interface
    @property
    def commands(self):
        """
        Generate the (tag, size, offset) triple of every load command in this image

        The offset is absolute within the file, so a caller that recognizes a tag can
        read the rest of the command straight from my contents
        """
        # the load commands follow the header
        offset = self.base + self.headerSize
        # walk the table
        for _ in range(self.count):
            # every command opens with its tag and its extent
            tag, size = self.unpack("2I", offset)
            # a command that doesn't advance would spin us forever
            if size < 8:
                # so treat it as damage
                raise self.FormatError(path=self.path, problem="degenerate load command")
            # hand over the command, with the linker's attention bit masked off
            yield tag & ~self.required, size, offset
            # and step over it
            offset += size
        # all done
        return

    @property
    def dependencies(self):
        """
        Generate the names of the shared libraries this image loads
        """
        # go through the load commands
        for tag, size, offset in self.commands:
            # skipping the ones that name no library
            if tag not in self.imports:
                # by moving on
                continue
            # the name is an offset from the start of the command
            name, = self.unpack("I", offset + 8)
            # which must land inside it
            if name >= size:
                # or the command is damaged
                raise self.FormatError(path=self.path, problem="bad dylib name offset")
            # read the string it points at
            yield self.string(offset=offset + name)
        # all done
        return

    @property
    def soname(self):
        """
        The install name this image announces itself by, or {None} when it has none
        """
        # go through the load commands
        for tag, size, offset in self.commands:
            # looking for the one that carries the identity
            if tag != self.identity:
                # and ignoring the rest
                continue
            # the name is an offset from the start of the command
            name, = self.unpack("I", offset + 8)
            # read the string it points at
            return self.string(offset=offset + name)
        # executables carry no install name
        return None

    # meta-methods
    def __init__(self, cputype=None, **kwds):
        """
        Read a mach-o image, selecting the slice for {cputype} out of a universal file
        """
        # chain up to pull the contents
        super().__init__(**kwds)
        # read the leading word in the order the thin magics are written on disk
        leading = int.from_bytes(self.data[:4], "little")
        # universal files wrap the images in a big endian table of contents
        if leading in (self.fat, self.fatSwapped):
            # locate the slice we care about
            self.base = self.slice(cputype=cputype)
        # everything else is a single image at the top of the file
        else:
            # so it starts where the file does
            self.base = 0

        # read its magic, in the byte order the file was written in
        magic = int.from_bytes(self.data[self.base : self.base + 4], "little")
        # the byte swapped magics say the image was written on the other kind of machine
        self.order = self.big if magic in (self.cigam32, self.cigam64) else self.little
        # normalize the byte swapped forms so the width test below sees one spelling
        magic = {self.cigam32: self.magic32, self.cigam64: self.magic64}.get(magic, magic)
        # anything else is not a mach-o image
        if magic not in (self.magic32, self.magic64):
            # so complain
            raise self.FormatError(path=self.path, problem="not a mach-o image")
        # the 64 bit header carries one reserved word the 32 bit header doesn't
        self.headerSize = 32 if magic == self.magic64 else 28
        # the command count is the fifth word of the header
        self.count, = self.unpack("I", self.base + 16)
        # all done
        return

    # implementation details
    def slice(self, cputype):
        """
        Find the offset of the slice for {cputype} within a universal file, or of the
        first slice when the caller doesn't care
        """
        # the table of contents is big endian regardless of the machine
        self.order = self.big
        # its second word counts the images that follow
        count, = self.unpack("I", 4)
        # a universal file with no images is useless
        if not count:
            # so complain
            raise self.FormatError(path=self.path, problem="universal file with no images")
        # go through the table entries, which follow the two word header
        for index in range(count):
            # each one describes a slice in five words
            entry = 8 + index * 20
            # whose first word names the architecture and whose third locates the image
            architecture, _, offset, _, _ = self.unpack("5I", entry)
            # take the first slice when the caller has no preference, or the match
            if cputype is None or architecture == cputype:
                # and hand back where the image begins
                return offset
        # the file carries no image for the requested architecture
        raise self.FormatError(path=self.path, problem=f"no slice for cputype {cputype}")


# end of file
