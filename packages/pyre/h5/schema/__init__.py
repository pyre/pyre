# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# the local exceptions
from . import exceptions

# the metaclass
from .Schema import Schema as schema

# the structural elements
from .Descriptor import Descriptor as descriptor
from .Group import Group as group
from .Root import Root as root
from .Dataset import Dataset as dataset
from .Dimension import Dimension as dimension

# a visitor that displays the structure of a schema
from .Viewer import Viewer as viewer

# the typed descriptors
# scalars
bool = dataset.bool  # booleans
complex = dataset.complex  # complex numbers
enum = dataset.enum  # enumerations
float = dataset.float  # floats
int = dataset.int  # integers
iq = dataset.iq  # radar samples, a pair of integer counts
str = dataset.str  # strings
timestamp = dataset.timestamp  # timestamps
# containers
array = dataset.array  # arrays of cells
list = dataset.list  # lists
tuple = dataset.tuple  # tuples
# derived
from ..typed.Strings import Strings as strings


# convenience schema factory
def make(name, bases=(group,), attributes={}, **kwds):
    """
    Make a new schema class
    """
    # easy enough
    return schema(name, bases, attributes, **kwds)


# end of file
