# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# superclass
from .Location import Location

# typing
import typing


# a basic h5 object
class Object(Location):
    """
    The base class for all h5 objects

    This is the home of the descriptor protocol implementation that makes it possible to
    give groups their contents
    """

    # descriptor support
    def __set_name__(self, cls: type, name: str) -> None:
        """
        Attach my name
        """
        # bind me to my name
        self.pyre_bind(name=name)
        # all done
        return

    def __get__(self, instance: "Object", cls: type) -> typing.Any:
        """
        Read access to my value
        """
        # when accessing through a class record
        if instance is None:
            # return the descriptor
            return self
        # otherwise, ask the {instance}
        return instance.pyre_get(name=self.pyre_name)

    def __set__(self, instance: "Object", value: typing.Any) -> None:
        """
        Write access to my value
        """
        # attach it to {instance}
        instance.pyre_set(name=self.pyre_name, value=value)
        # all done
        return

    def __delete__(self, instance: "Object") -> None:
        """
        Delete my value
        """
        # remove my value from {instance}
        instance.pyre_delete(name=self.pyre_name)
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

    # the default implementations of the content accessors
    def pyre_get(self, **kwds):
        # not implemented
        raise NotImplementedError(
            f"class '{type(self).__name__}' must implement 'pyre_get'"
        )

    def pyre_set(self, **kwds):
        # not implemented
        raise NotImplementedError(
            f"class '{type(self).__name__}' must implement 'pyre_set'"
        )

    def pyre_delete(self, **kwds):
        # not implemented
        raise NotImplementedError(
            f"class '{type(self).__name__}' must implement 'pyre_delete'"
        )


# end of file
