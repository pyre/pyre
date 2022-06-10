#-*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2022 all rights reserved


# basic objects
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


# the explorer
from .Tree import Tree as tree


# end of file
