# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# superclass
from .Location import Location


# a basic h5 object
class Object(Location):
    """
    The base class for all h5 objects

    This is the home of the descriptor protocol implementation that makes it possible to
    give groups their contents
    """

    # descriptor support
    def __set_name__(self, cls: type, name: str):
        """
        Attach my name
        """
        # bind my to my name
        self.pyre_bind(name=name)
        # all done
        return

    def __get__(self, group: "pyre.h5.Group", cls: type):
        """
        Read access to my value
        """
        # when accessing through a class record
        if group is None:
            # return the descriptor
            return self
        # otherwise, ask the {group} for my value manager
        identifier = group.pyre_get(name=self.pyre_name)
        # and make it available
        return identifier

    def __set__(self, group: "pyre.h5.Group", identifier: "Identifier"):
        """
        Write access to my value
        """
        # and attach it to {instance}
        group.pyre_set(name=self.pyre_name, identifier=identifier)
        # all done
        return

    def __delete__(self, group: "pyre.h5.Group"):
        """
        Delete my value
        """
        # remove my value from {instance}
        group.pyre_delete(descriptor=self)
        # and done
        return

    # framework hooks
    def pyre_identify(self, authority, **kwds):
        """
        Let {authority} know i am an object
        """
        # attempt to
        try:
            # ask {authority} for my handler
            handler = authority.pyre_onObject
        # if it doesn't understand
        except AttributeError:
            # chain up
            return super().pyre_identify(authority=authority, **kwds)
        # otherwise, invoke the handler
        return handler(object=self, **kwds)


# end of file
