# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# support
import journal

# metaclass
from .Schema import Schema

# superclass
from .Descriptor import Descriptor

# parts
from .Inventory import Inventory

# typing
import typing
from .Dataset import Dataset

# the composite node
class Group(Descriptor, metaclass=Schema):
    """
    A container of datasets
    """

    # metamethods
    def __init__(self, descriptors=None, **kwds):
        # chain up
        super().__init__(**kwds)
        # normalize the explicit contents
        if descriptors is None:
            # by making sure its a mappint
            descriptors = {}
        # deduce my schema: grab the class descriptors and add the explicit content
        descriptors = Inventory(**type(self)._pyre_descriptors, **descriptors)
        # grab my attributes
        attributes = self.__dict__
        # prep my content
        content = {}
        # go through the schema
        for name, descriptor in descriptors.items():
            # clone the source {descriptor} to decouple my state
            clone = descriptor._pyre_clone()
            # add it to my pile
            content[name] = clone
            # if {name} does not correspond to a known attribute
            if name not in attributes:
                # add it
                attributes[name] = clone
        # attach my contents
        self._pyre_descriptors = content
        # all done
        return

    def _disable__getattr__(self, name: str) -> typing.Any:
        """
        Trap failures in attribute lookup to support dynamic content
        """
        print(f"pyre.h5.schema.Group.__getattr__: {name=}")
        # check whether
        try:
            # {name} points to one of my dynamic identifiers, in which case grab the value
            value = self._pyre_get(name=name)
        # if not
        except KeyError:
            # i'm out of ideas; must have been a typo
            raise AttributeError(f"group '{self._pyre_name}' has no member '{name}'")
        # if it's there
        return value

    def __setattr__(self, name: str, value: typing.Any) -> None:
        """
        Trap assignments unconditionally
        """
        # get my descriptors
        descriptors = self._pyre_descriptors
        # check whether
        try:
            # {name} is a known {descriptor}
            descriptor = descriptors[name]
        # if not
        except KeyError:
            # if {value} is not a descriptor
            if not isinstance(value, Descriptor):
                # chain up to handle a normal assignment
                return super().__setattr__(name, value)
            # otherwise, register it as a known descriptor
            descriptors[name] = value
            # record it
            self.__dict__[name] = value
            # bind it
            value._pyre_bind(name=name)
            # and done
            return
        # for known descriptors, the following cases are possible:
        # if {descriptor} is a {dataset} and {value} is not a descriptor
        if isinstance(descriptor, Dataset) and not isinstance(value, Descriptor):
            # interpret as setting a new default value
            descriptor.default = value
            # all done
            return
        # if {value} is not a descriptor
        if not isinstance(value, Descriptor):
            # this is almost certainly a bug; make a channel
            channel = journal.firewall("pyre.h5.schema")
            # build a report
            channel.line(
                f"unsupported assignment '{self._pyre_name}.{name}' <- {value}"
            )
            channel.line(f"to {self}")
            # flush
            channel.log()
            # and bail, just in case firewalls aren't fatal
            return
        # otherwise, replace my {descriptor} with {value}
        descriptors[name] = value
        # bind it
        value._pyre_bind(name=name)
        # all done
        return

    # representation
    def __str__(self) -> str:
        """
        Human readable description
        """
        # unpack my info
        name = self._pyre_name
        # and the info of my type
        cls = type(self)
        module = cls.__module__
        typename = cls.__name__
        # put it all together
        return f"group '{name}', an instance of '{module}.{typename}'"

    # framework hooks
    def _pyre_get(self, name: str) -> typing.Any:
        """
        Look up my value for {name}
        """
        # N.B. this hook is invoked both from the named descriptor's {__get__} for static
        # content, and my {__getattr__}, when normal look up fails. both of these paths
        # handle failures to find a matching descriptor, so there is no need to do it here.
        # so, lookup the descriptor that is associated with {name}
        return self._pyre_descriptors[name]


# end of file
