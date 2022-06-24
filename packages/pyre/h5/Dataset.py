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


    # public data
    @property
    def pyre_marker(self):
        """
        Generate an identifying mark
        """
        # use my type name
        return self.typename


    # metamethods
    def __str__(self):
        """
        Human readable representation
        """
        # easy enough
        return f"a dataset of type '{self.typename}'"


    # framework hooks
    def pyre_sync(self, **kwds):
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


    def pyre_identify(self, authority, **kwds):
        """
        Let {authority} know i am a dataset
        """
        # attempt to
        try:
            # ask {authority} for my handler
            handler = authority.pyre_onDataset
        # if it doesn't exist
        except AttributeError:
            # chain up
            return super().pyre_identify(authority=authority, **kwds)
        # otherwise, invoke the handler
        return handler(dataset=self, **kwds)


# end of file
