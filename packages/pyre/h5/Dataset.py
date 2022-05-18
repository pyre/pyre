#-*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2022 all rights reserved


# superclass
from .Object import Object
# type information
from .. import schemata


# the dataset descriptor base class
@schemata.typed
class Dataset(Object):
    """
    The base class of all dataset descriptors
    """


    # metamethods
    def __str__(self):
        """
        Human readable representation
        """
        # easy enough
        return f"a dataset of type '{self.typename}'"


# end of file
