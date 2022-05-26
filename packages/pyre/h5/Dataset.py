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


    # framework hooks
    def pyre_sync(self):
        """
        Hook invoked when the {inventory} lookup fails and a value must be generated
        """
        # chain up to give my ancestors a chance to chip in
        value = super().pyre_sync()
        # if they have no opinion
        if value is None:
            # use my default
            value = self.default
        # and that's all i can do
        return value


    def pyre_process(self, value, **kwds):
        """
        Walk {value} through my transformations
        """
        # let my {type} do the work
        return self.process(value=value, **kwds)


# end of file
