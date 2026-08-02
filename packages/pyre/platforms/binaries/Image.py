# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# externals
import struct


# the base of the binary image readers
class Image:
    """
    The base class for readers of loadable binary images

    An image is an executable or shared library on disk. Subclasses know one container
    format each and parse its structure; they expose the raw structure they walked, so
    that extracting information the base interface doesn't name is a matter of reading
    the parsed table rather than teaching the reader a new trick
    """

    # exceptions
    from .exceptions import FormatError

    # constants
    # the byte order markers, as {struct} spells them
    little = "<"
    big = ">"

    # class interface
    @classmethod
    def claims(cls, data):
        """
        Check whether this reader recognizes the image whose leading bytes are in {data}
        """
        # subclasses know their own magic
        raise NotImplementedError(
            f"class '{cls.__name__}' must implement 'claims'"
        )

    # interface
    @property
    def dependencies(self):
        """
        Generate the names of the shared libraries this image loads
        """
        # subclasses know where their format records them
        raise NotImplementedError(
            f"class '{type(self).__name__}' must implement 'dependencies'"
        )

    @property
    def soname(self):
        """
        The name this image announces itself by, or {None} when it doesn't
        """
        # subclasses that can answer override this
        return None

    # implementation details
    def unpack(self, format, offset):
        """
        Read the fields described by {format} from my contents, starting at {offset}
        """
        # splice my byte order onto the caller's format
        spec = f"{self.order}{format}"
        # compute the extent of the read
        size = struct.calcsize(spec)
        # if it runs past the end of the image
        if offset + size > len(self.data):
            # the file is damaged or lied about its geometry
            raise self.FormatError(path=self.path, problem="truncated image")
        # unpack the fields
        return struct.unpack_from(spec, self.data, offset)

    def string(self, offset):
        """
        Read the null terminated string that starts at {offset} in my contents
        """
        # find the terminator
        end = self.data.find(b"\0", offset)
        # a string that never ends means the file is damaged
        if end < 0:
            # so complain
            raise self.FormatError(path=self.path, problem="unterminated string")
        # carve out the bytes and render them; image tables are ascii by construction,
        # but a corrupt file shouldn't raise on decode, so be forgiving
        return self.data[offset:end].decode("utf-8", errors="replace")

    # meta-methods
    def __init__(self, path, data=None, **kwds):
        """
        Read the image at {path}, or interpret {data} as its contents
        """
        # chain up
        super().__init__(**kwds)
        # record where the image lives
        self.path = path
        # pull its contents, unless the caller supplied them
        self.data = open(str(path), "rb").read() if data is None else data
        # the byte order, which subclasses deduce from the magic
        self.order = self.little
        # all done
        return

    # debugging support
    def __str__(self):
        # identify myself by format and location
        return f"{type(self).__name__} image at '{self.path}'"


# end of file
