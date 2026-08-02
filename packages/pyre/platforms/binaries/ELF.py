# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# superclass
from .Image import Image


# the reader of elf images
class ELF(Image):
    """
    A reader of the elf images used by linux and the other u*ix platforms

    The dynamic linker finds everything it needs through the program headers, so this
    reader does the same and never looks at the section table, which is routinely
    stripped. {segments} hands over the program headers and {dynamic} the entries of the
    dynamic table, so mining a tag this class doesn't interpret means matching on it
    rather than parsing the container again
    """

    # constants
    # the four bytes every elf image opens with
    magic = b"\x7fELF"

    # the classes, as the identification bytes spell them
    elf32 = 1
    elf64 = 2
    # and the byte orders
    lsb = 1
    msb = 2

    # the program header kinds this reader cares about
    load = 1  # PT_LOAD: a segment the loader maps, hence an address to offset anchor
    dynamicSegment = 2  # PT_DYNAMIC: the table the dynamic linker reads

    # the dynamic tags
    end = 0  # DT_NULL: terminates the table
    needed = 1  # DT_NEEDED: names a shared library to load
    strtab = 5  # DT_STRTAB: locates the string table the names live in
    identity = 14  # DT_SONAME: the name the image announces itself by
    rpath = 15  # DT_RPATH: the legacy search path
    runpath = 29  # DT_RUNPATH: the search path that supersedes it

    # class interface
    @classmethod
    def claims(cls, data):
        """
        Check whether {data} opens with the elf identification bytes
        """
        # easy enough
        return data[:4] == cls.magic

    # interface
    @property
    def segments(self):
        """
        Generate the (kind, offset, address, extent) tuple of every program header
        """
        # walk the table
        for index in range(self.count):
            # locate this entry
            entry = self.headers + index * self.stride
            # the 64 bit layout puts the flags right after the kind
            if self.width == self.elf64:
                # so read past them
                kind, _, offset, address, _, extent = self.unpack("2I4Q", entry)
            # the 32 bit layout keeps the flags at the end, out of our way
            else:
                # so the fields we want come first
                kind, offset, address, _, extent = self.unpack("5I", entry)
            # hand over the segment
            yield kind, offset, address, extent
        # all done
        return

    @property
    def dynamic(self):
        """
        Generate the (tag, value) pair of every entry in the dynamic table
        """
        # find the segment that carries the table
        table = next(
            (offset for kind, offset, _, _ in self.segments if kind == self.dynamicSegment),
            None,
        )
        # a statically linked image has no dynamic table at all
        if table is None:
            # and therefore nothing to say
            return
        # the entries are a tag and a value, in the image's word size
        format, stride = ("2Q", 16) if self.width == self.elf64 else ("2I", 8)
        # walk the table
        while True:
            # read the entry
            tag, value = self.unpack(format, table)
            # the null tag ends the table
            if tag == self.end:
                # so we are done
                break
            # hand it over
            yield tag, value
            # and step to the next one
            table += stride
        # all done
        return

    @property
    def dependencies(self):
        """
        Generate the names of the shared libraries this image loads
        """
        # collect the dynamic table once, since we walk it twice
        entries = tuple(self.dynamic)
        # locate the string table the names live in
        strings = self.strings(entries=entries)
        # an image with no string table can name nothing
        if strings is None:
            # so there is nothing to report
            return
        # go through the entries
        for tag, value in entries:
            # looking for the ones that name a library
            if tag == self.needed:
                # whose value is an offset into the string table
                yield self.string(offset=strings + value)
        # all done
        return

    @property
    def soname(self):
        """
        The name this image announces itself by, or {None} when it has none
        """
        # collect the dynamic table
        entries = tuple(self.dynamic)
        # locate the string table
        strings = self.strings(entries=entries)
        # without one there is no name to read
        if strings is None:
            # so report failure
            return None
        # go through the entries
        for tag, value in entries:
            # looking for the identity
            if tag == self.identity:
                # whose value is an offset into the string table
                return self.string(offset=strings + value)
        # executables and unversioned libraries carry no soname
        return None

    @property
    def searchpath(self):
        """
        Generate the entries of the run time library search path baked into this image
        """
        # collect the dynamic table
        entries = tuple(self.dynamic)
        # locate the string table
        strings = self.strings(entries=entries)
        # without one there is no path to read
        if strings is None:
            # so there is nothing to report
            return
        # go through the entries
        for tag, value in entries:
            # both the modern search path and the legacy one carry the same payload
            if tag in (self.runpath, self.rpath):
                # a colon separated list at an offset into the string table
                yield from self.string(offset=strings + value).split(":")
        # all done
        return

    # meta-methods
    def __init__(self, **kwds):
        """
        Read an elf image
        """
        # chain up to pull the contents
        super().__init__(**kwds)
        # a file that doesn't open with the identification bytes is not one of ours
        if not self.claims(self.data):
            # so complain
            raise self.FormatError(path=self.path, problem="not an elf image")
        # the fifth byte says whether the image is 32 or 64 bit
        self.width = self.data[4]
        # which must be one of the two the format defines
        if self.width not in (self.elf32, self.elf64):
            # or the file is damaged
            raise self.FormatError(path=self.path, problem="unknown elf class")
        # the sixth byte says which end the words are written from
        self.order = self.big if self.data[5] == self.msb else self.little
        # the program header table is located differently in the two layouts
        if self.width == self.elf64:
            # its offset is a full word at the fifth field of the header
            self.headers, = self.unpack("Q", 32)
            # and its geometry sits further along
            self.stride, self.count = self.unpack("2H", 54)
        # the 32 bit header packs the same fields into narrower slots
        else:
            # so the offset lands earlier
            self.headers, = self.unpack("I", 28)
            # as does the geometry
            self.stride, self.count = self.unpack("2H", 42)
        # all done
        return

    # implementation details
    def strings(self, entries):
        """
        Find the file offset of the dynamic string table described by {entries}
        """
        # look for the tag that locates it
        address = next((value for tag, value in entries if tag == self.strtab), None)
        # an image without one cannot name anything
        if address is None:
            # so report failure
            return None
        # the tag records a load address, which we resolve against the mapped segments
        return self.resolve(address=address)

    def resolve(self, address):
        """
        Convert a load {address} into an offset into my contents
        """
        # go through the segments the loader maps
        for kind, offset, base, extent in self.segments:
            # ignoring the ones that never make it into memory
            if kind != self.load:
                # by moving on
                continue
            # if the address falls inside this one
            if base <= address < base + extent:
                # shift it by the distance between the segment's two addresses
                return offset + (address - base)
        # an address that no segment maps means the image is damaged
        raise self.FormatError(path=self.path, problem=f"unmapped address {address:#x}")


# end of file
