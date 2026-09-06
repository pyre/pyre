# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Support for ENVI headers, the text sidecars that describe flat binary rasters.

An ENVI header is a text file of {keyword = value} entries, with braces around values that have
several items or contain spaces. The standard keywords are known here by name and type, and
land on the traits of {header}; anything else lands in its {extras} bag as text, a string for a
bare value and a list of strings for a braced one, for the consumer to interpret.

The sequence

    import pyre
    import pyre.grid
    hdr = pyre.envi.reader().read(uri="product.hdr")
    data = pyre.grid.map(uri="product", shape=hdr.shape, cell=hdr.cell, create=False)

reads a header and lays a grid over the product it describes, in place, whatever byte order the
product was written in; {writer} renders a header back to text.
"""

# the exceptions
from . import exceptions

# the header
from .Header import Header as header

# the georeferencing record
from .MapInfo import MapInfo as mapInfo

# reading and writing
from .Reader import Reader as reader
from .Writer import Writer as writer

# end of file
