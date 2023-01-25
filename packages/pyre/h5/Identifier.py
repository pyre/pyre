# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# typing
import pyre
import typing


# base class of all h5 objects
class Identifier:
    """
    A placeholder for h5 identifiers, a very very low level concept
    """

    # interface
    def pyre_close(self) -> "Identifier":
        """
        Detach me from my HDF5 object
        """
        # get my id
        hid = self.pyre_id
        # if it's valid
        if hid is not None:
            # close it
            hid.close()
            # reset my id
            self.pyre_id = None
        # all done
        return self

    # metamethods
    def __init__(
        self,
        id: typing.Any = None,
        name: typing.Optional[str] = None,
        doc: typing.Optional[str] = None,
        **kwds,
    ):
        # chain up
        super().__init__(**kwds)
        # the handle to my HDF% object
        self.pyre_id = id
        # my name
        self.pyre_name: str = name
        # my docstring
        self.pyre_doc: str = doc
        # all done
        return

    def __del__(self):
        # detach me from my h5 object
        self.pyre_close()
        # all done
        return

    # rep
    def __str__(self):
        """
        Human readable representation
        """
        # easy enough
        return "an identifier"

    # framework hooks
    def pyre_bind(self, name: str):
        """
        Bind me to my {name}
        """
        # save my name
        self.pyre_name = name
        # all done
        return

    def pyre_clone(
        self,
        id: typing.Optional[typing.Any] = None,
        name: typing.Optional[str] = None,
        **kwds,
    ):
        """
        Make as faithful a clone of mine as possible
        """
        # if the caller did not specify an id
        if id is None:
            # use mine
            id = self.pyre_id
        # if the caller did not express any opinions on the name
        if name is None:
            # use mine
            name = self.pyre_name
        # invoke my constructor
        return type(self)(id=id, name=name, doc=self.pyre_doc, **kwds)

    def pyre_identify(self, authority, **kwds):
        """
        Let {authority} know i am an identifier
        """
        # attempt to
        try:
            # ask authority for the base handler
            handler = authority.pyre_onIdentifier
        # if it doesn't understand
        except AttributeError:
            # it's not a visitor
            raise NotImplementedError(
                f"class '{type(authority).__name__}' is not a '{type(self).__name__}' visitor"
            )
        # otherwise, invoke the hook
        return handler(identifier=self, **kwds)


# end of file
