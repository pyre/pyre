# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# typing
import typing


# base class of all h5 objects
class Identifier:
    """
    A placeholder for h5 identifiers, a very very low level concept
    """

    # interface
    def _pyre_close(self) -> "Identifier":
        """
        Detach me from my HDF5 object
        """
        # get my id
        hid = self._pyre_id
        # if it's valid
        if hid is not None:
            # close it
            hid.close()
            # reset my id
            self._pyre_id = None
        # all done
        return self

    # metamethods
    def __init__(
        self,
        id: typing.Any = None,
        **kwds,
    ):
        # chain up
        super().__init__(**kwds)
        # the handle to my HDF% object
        self._pyre_id = id
        # all done
        return

    def __del__(self):
        # detach me from my h5 object
        self._pyre_close()
        # all done
        return

    # rep
    def __str__(self):
        """
        Human readable representation
        """
        # easy enough
        return f"an identifier"

    # framework hooks
    # visiting
    def _pyre_identify(self, authority, **kwds):
        """
        Let {authority} know i am an identifier
        """
        # attempt to
        try:
            # ask authority for the base handler
            handler = authority._pyre_onIdentifier
        # if it doesn't understand
        except AttributeError:
            # get my class
            cls = type(self)
            # and my poorly formed visitor
            visitor = type(authority)
            # it's not a visitor, since we only get here when all alternatives are exhausted
            raise NotImplementedError(
                f"class '{visitor.__module__}.{visitor.__name__}' "
                f"is not a '{cls.__module__}.{cls.__name__}' visitor"
            )
        # otherwise, invoke the hook
        return handler(identifier=self, **kwds)


# end of file