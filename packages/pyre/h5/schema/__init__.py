# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2024 all rights reserved


# the local exceptions
from . import exceptions

# the metaclass
from .Schema import Schema as schema

# the structural elements
from .Descriptor import Descriptor as descriptor
from .Group import Group as group
from .Dataset import Dataset as dataset

# a visitor that displays the structure of a schema
from .Viewer import Viewer as viewer

# the typed descriptors
# scalars
bool = dataset.bool
complex = dataset.complex
float = dataset.float
int = dataset.int
str = dataset.str
timestamp = dataset.timestamp
# containers
array = dataset.array
list = dataset.list
tuple = dataset.tuple
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
