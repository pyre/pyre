# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# publish
from .Descriptor import Descriptor as descriptor
from .Group import Group as group
from .Dataset import Dataset as dataset

# the typed descriptors
# scalars
bool = dataset.bool
float = dataset.float
int = dataset.int
str = dataset.str
timestamp = dataset.timestamp
# containers
array = dataset.array
list = dataset.list
tuple = dataset.tuple
# derived
from .Strings import Strings as strings


# end of file
