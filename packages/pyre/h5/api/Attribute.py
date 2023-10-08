# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# external
import pyre
import journal

# superclass
from .Location import Location

# typing
import typing


# attributes
class Attribute(Location):
    """
    Access to attribute values
    """

    # properties
    @property
    def name(self):
        """
        Get my name
        """
        # easy enough
        return self._pyre_id.name

    # metadata
    @property
    def cell(self):
        """
        The dataset cell type, a DataSetType enum
        """
        # easy enough
        return self._pyre_id.cell

    @property
    def disksize(self):
        """
        The on-disk size of the dataset
        """
        # easy enough
        return self._pyre_id.disksize

    @property
    def memsize(self):
        """
        The in-memory size of the dataset
        """
        # easy enough
        return self._pyre_id.memsize

    @property
    def shape(self):
        """
        The dataset shape
        """
        # easy enough
        return self._pyre_id.shape

    @property
    def space(self):
        """
        The dataset space
        """
        # easy enough
        return self._pyre_id.space

    @property
    def type(self):
        """
        The dataset type
        """
        # easy enough
        return self._pyre_id.type

    # visiting
    def _pyre_identify(self, authority, **kwds):
        """
        Let {authority} know i am an attribute
        """
        # attempt to
        try:
            # ask {authority} for my handler
            handler = authority._pyre_onAttribute
        # if it doesn't understand
        except AttributeError:
            # chain up
            return super()._pyre_identify(authority=authority, **kwds)
        # otherwise, invoke the handler
        return handler(dataset=self, **kwds)


# end of file
