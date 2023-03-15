# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# support
import itertools
import typing

# metaclass
from .Schema import Schema

# superclass
from .Descriptor import Descriptor

# parts
from .Inventory import Inventory


# the composite node
class Group(Descriptor, metaclass=Schema):
    """
    A container of datasets
    """

    # metamethods
    def __init__(self, **kwds):
        # chain up
        super().__init__(**kwds)
        # initialize the storage for my dynamic content
        self._pyre_instanceDescriptors = Inventory()
        # initialize my table with the h5 names of my members
        self._pyre_aliases = dict(self._pyre_staticAliases)
        # all done
        return

    # attribute setting
    def __setattr__(self, name: str, value: typing.Any) -> None:
        # if value is a named descriptor
        if isinstance(value, Descriptor) and value._pyre_name is not None:
            # add the attribute name to my pile of known descriptors
            self._pyre_instanceDescriptors.add(name)
            # and the name of the descriptor to my aliases
            self._pyre_aliases[value._pyre_name] = name
        # chain up to carry out the actual assignment
        return super().__setattr__(name, value)

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
    # introspection
    def _pyre_descriptors(self):
        """
        Generate a sequence of my descriptors
        """
        # throw all descriptor name into a pile
        names = set(
            itertools.chain(self._pyre_instanceDescriptors, self._pyre_classDescriptors)
        )
        # go through them
        for name in names:
            # retrieve the associated value
            attr = getattr(self, name)
            # the user may have reassigned an non-descriptor to this {name}, so let's
            # verify that what we retrieved is a descriptor
            if isinstance(attr, Descriptor):
                # we got one; send it off
                yield attr
        # all done
        return

    def _pyre_find(self, alias):
        """
        Find the descriptor with the given {name}
        """
        # lookup the name in my aliases
        name = self._pyre_aliases[alias]
        # retrieve my attribute
        attr = getattr(self, name)
        # if it's not a descriptor
        if not isinstance(attr, Descriptor):
            # bail
            raise KeyError(f"'{alias}' is not a descriptor in {self}")
        # otherwise, return it
        return attr

    # visiting
    def _pyre_identify(self, authority, **kwds):
        """
        Let {authority} know i am a group
        """
        # attempt to
        try:
            # ask {authority} for my handler
            handler = authority._pyre_onGroup
        # if it doesn't understand
        except AttributeError:
            # chain up
            return super()._pyre_identify(authority=authority, **kwds)
        # otherwise, invoke the handler
        return handler(group=self, **kwds)

    # decoration
    def _pyre_marker(self):
        """
        Generate an identifying mark for structural renderings
        """
        # easy
        return "g"


# end of file
