# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# superclass
from .Object import Object


# a basic h5 object
class Dataset(Object):
    """
    Access to the data stored in an h5 file
    """

    # datasets are scalars, by default
    shape = "scalar"

    # value access
    @property
    def value(self):
        """
        Retrieve my value
        """
        # easy enough
        return self._value

    @value.setter
    def value(self, value):
        """
        Store my value
        """
        # process the incoming value and store it
        self._value = self._pyre_layout.process(value)
        # all done
        return

    # metamethods
    def __init__(self, layout=None, **kwds):
        # chain up
        super().__init__(layout=layout, **kwds)
        # initialize my value
        self._value = layout.process(layout.default)
        # all done
        return

    def __str__(self):
        """
        Human readable representation
        """
        # easy enough
        return (
            f"dataset at '{self.pyre_location}', a {self.shape} of type '{self.type}'"
        )

    # framework hooks
    def _pyre_identify(self, authority, **kwds):
        """
        Let {authority} know i am a dataset
        """
        # attempt to
        try:
            # ask {authority} for my handler
            handler = authority._pyre_onDataset
        # if it doesn't understand
        except AttributeError:
            # chain up
            return super()._pyre_identify(authority=authority, **kwds)
        # otherwise, invoke the handler
        return handler(dataset=self, **kwds)


# end of file
