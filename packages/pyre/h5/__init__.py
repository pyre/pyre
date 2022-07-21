# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2022 all rights reserved


# internals that mirror the h5 C++ api
from .Identifier import Identifier as identifier
from .Location import Location as location
from .Object import Object as object

# structural objects
from .Group import Group as group
from .File import File as file


# datasets
from .Dataset import Dataset as dataset

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

# containers
from .typed.Strings import Strings as strings


# readers and writers
from .Reader import Reader as reader
from .Writer import Writer as writer

# visitors
from .Explorer import Explorer as explorer
from .Tree import Tree as tree
from .Walker import Walker as walker


# end of file
