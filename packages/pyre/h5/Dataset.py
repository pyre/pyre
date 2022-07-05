# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2022 all rights reserved


# support
import pyre

# superclass
from .Object import Object


# the dataset descriptor base class
@pyre.schemata.typed
class Dataset(Object):
    """
    The base class of all dataset descriptors
    """

    # public data
    @property
    def value(self):
        """
        Retrieve my value
        """
        # get the value from my cache
        value = self._value
        # and return it
        return value

    @value.setter
    def value(self, value):
        """
        Set my value
        """
        # process and cache the result
        self._value = self.process(value=value)
        # and done
        return

    @property
    def pyre_marker(self):
        """
        Generate an identifying mark
        """
        # use my type name
        return self.typename

    # metamethods
    def __init__(self, **kwds):
        # chain up
        super().__init__(**kwds)
        # set up my {value}
        self._value = self.process(value=self.default)
        # all done
        return

    def __str__(self):
        """
        Human readable representation
        """
        # easy enough
        return f"{self.pyre_location}: a dataset of type '{self.typename}'"

    # framework hooks
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

    def pyre_clone(self, **kwds):
        """
        Make as faithful a clone of mine as possible
        """
        # invoke my constructor
        return super().pyre_clone(default=self.default, **kwds)


# end of file
