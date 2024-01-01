# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2024 all rights reserved


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
        The attribute cell type, a DataSetType enum
        """
        # easy enough
        return self._pyre_id.cell

    @property
    def disksize(self):
        """
        The on-disk size of the attribute
        """
        # easy enough
        return self._pyre_id.disksize

    @property
    def memsize(self):
        """
        The in-memory size of the attribute
        """
        # easy enough
        return self._pyre_id.memsize

    @property
    def shape(self):
        """
        The attribute shape
        """
        # easy enough
        return self._pyre_id.shape

    @property
    def space(self):
        """
        The attribute space
        """
        # easy enough
        return self._pyre_id.space

    @property
    def type(self):
        """
        The attribute type
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
        return handler(attribute=self, **kwds)


# end of file
