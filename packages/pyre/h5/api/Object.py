# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2024 all rights reserved


# superclass
from .Location import Location

# my parts
from .Attribute import Attribute

# typing
import typing
from .. import schema


# a basic h5 object
class Object(Location):
    """
    The base class for all publicly visible h5 objects
    """

    # metamethods
    def __init__(self, layout: typing.Optional[schema.descriptor] = None, **kwds):
        # chain up
        super().__init__(**kwds)
        # record my type
        self._pyre_layout = layout
        # all done
        return

    # interface
    # attribute access
    def _pyre_attributes(self):
        """
        Retrieve the names of all the attributes
        """
        # easy enough
        return self._pyre_id.attributes()

    def _pyre_attribute(self, name):
        """
        Retrieve the attribute with the given {name}
        """
        # retrieve the attribute handle
        id = self._pyre_id.getAttribute(name=name)
        # dress it up and return
        return Attribute(id=id)

    def _pyre_hasAttribute(self, name):
        """
        Check whether an attribute by the given {name} exists
        """
        # easy enough
        return self._pyre_id.hasAttribute(name=name)

    def _pyre_createAttribute(self):
        """
        Create an attribute given type and layout information
        """

    def _pyre_renameAttribute(self, old, new):
        """
        Rename the {old} attribute to {new}
        """
        # easy enough
        return self._pyre_id.renameAttribute(old=old, new=new)

    def _pyre_removeAttribute(self, name):
        """
        Remove the attribute with the given {name}
        """
        return self._pyre_id.removeAttribute(name=name)

    # framework hooks
    # properties
    @property
    def _pyre_objectType(self):
        """
        Look up my h5 identifier type
        """
        # my handle knows
        return self._pyre_id.objectType

    # visitor
    def _pyre_identify(self, authority, **kwds):
        """
        Let {authority} know i am an object
        """
        # attempt to
        try:
            # ask {authority} for my handler
            handler = authority._pyre_onObject
        # if it doesn't understand
        except AttributeError:
            # chain up
            return super()._pyre_identify(authority=authority, **kwds)
        # otherwise, invoke the handler
        return handler(object=self, **kwds)


# end of file
