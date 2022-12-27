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

    # metamethods
    def __init__(
        self,
        name: typing.Optional[str] = None,
        doc: typing.Optional[str] = None,
        **kwds
    ):
        # chain up
        super().__init__(**kwds)
        # my name
        self.pyre_name: str = name
        # my docstring
        self.pyre_doc: str = doc
        # all done
        return

    # descriptor support
    def __set_name__(self, cls: type, name: str):
        """
        Attach my name
        """
        # bind my to my name
        self.pyre_bind(name=name)
        # all done
        return

    def __get__(self, instance: "pyre.h5.Group", cls: type):
        """
        Read access to my value
        """
        # when accessing through a class record
        if instance is None:
            # return the descriptor
            return self
        # otherwise, aks {instance} for my value manager
        identifier = instance.pyre_get(descriptor=self)
        # and make it available
        return identifier

    def __set__(self, instance: "pyre.h5.Group", identifier: "Identifier"):
        """
        Write access to my value
        """
        # and attach it to {instance}
        instance.pyre_set(descriptor=self, identifier=identifier)
        # all done
        return

    def __delete__(self, instance: "pyre.h5.Group"):
        """
        Delete my value
        """
        # remove my value from {instance}
        instance.pyre_delete(descriptor=self)
        # and done
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

    def pyre_identify(self, authority, **kwds):
        """
        Let {authority} know i am an identifier
        """
        # invoke the hook
        return authority.pyre_onIdentifier(identifier=self, **kwds)

    def pyre_clone(self, name: typing.Optional[str] = None, **kwds):
        """
        Make as faithful a clone of mine as possible
        """
        # if the caller did not express any opinions
        if name is None:
            # use my name as the default
            name = self.pyre_name
        # invoke my constructor
        return type(self)(name=name, doc=self.pyre_doc, **kwds)


# end of file
