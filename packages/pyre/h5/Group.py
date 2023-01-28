# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# external
import itertools

# metaclass
from .Schema import Schema

# superclass
from .Object import Object

# my parts
from .Inventory import Inventory

# typing
import typing
from .Dataset import Dataset
from .Identifier import Identifier
from .Location import Location


# a dataset container
class Group(Object, metaclass=Schema):
    """
    A container of h5 objects
    """

    # public data
    @property
    def pyre_marker(self) -> str:
        """
        Generate an identifying mark
        """
        # use my type name
        return "g"

    # interface
    # access to contents by category
    def pyre_datasets(self) -> typing.Sequence[Dataset]:
        """
        Generate a sequence of my datasets
        """
        # filter and return
        return filter(lambda loc: issubclass(loc, Dataset), self.pyre_locations())

    def pyre_groups(self) -> typing.Sequence["Group"]:
        """
        Generate a sequence of my subgroups
        """
        # filter and return
        return filter(lambda loc: issubclass(loc, Group), self.pyre_locations())

    def pyre_locations(self) -> typing.Sequence[Location]:
        """
        Generate a sequence of contents
        """
        # nd off all known identifiers
        yield from self.pyre_identifiers.values()
        # all done
        return

    # metamethods
    def __init__(self, **kwds):
        # chain up
        super().__init__(**kwds)
        # initialize my inventory
        self.pyre_identifiers: Inventory = self.pyre_newInventory()
        # all done
        return

    def __getattr__(self, name: str) -> typing.Any:
        """
        Trap attribute look up to support dynamic identifiers
        """
        # N.B.: this get called after regular attribute lookup has failed, so we only get here
        # when {name} is not known to the static structure of a group
        # check whether
        try:
            # {name} points to one of my dynamic identifiers
            identifier = self.pyre_identifiers[name]
        # if not
        except KeyError:
            # i'm out of ideas
            raise AttributeError(
                f"group '{self.pyre_name}' has no identifier named '{name}'"
            )
        # otherwise, hand it off
        return identifier

    def __setattr__(self, name: str, value: typing.Any) -> None:
        """
        Trap attribute assignment unconditionally
        """
        # N.B.: unconditionally means unconditionally: this gets called during construction,
        # while the objet layout is being initialized;
        # so, during instantiation when my attributes are being initialized
        if name.startswith("pyre_"):
            # stay out of the way
            return super().__setattr__(name, value)
        # if {value} is not an {identifier}
        if not isinstance(value, Identifier):
            # chain up to process a normal assignment
            return super().__setattr__(name, value)
        # otherwise, make the assignment
        self.pyre_set(descriptor=value, identifier=value)
        # all done
        return

    def __str__(self) -> str:
        """
        Human readable description
        """
        # say something simple, for now
        return f"group '{self.pyre_name}' at '{self.pyre_location}'"

    # framework hooks
    def pyre_get(self, descriptor: Identifier) -> Identifier:
        """
        Look up the identifier associated this {descriptor}
        """
        # look up the {identifier} that corresponds to this descriptor
        identifier = self.pyre_identifiers[descriptor.pyre_name]
        # and return it
        return identifier

    def pyre_set(self, descriptor: Identifier, identifier: Identifier) -> None:
        """
        Associate my {descriptor} with {identifier}
        """
        # make the association
        self.pyre_identifiers[descriptor.pyre_name] = identifier
        # all done
        return

    def pyre_delete(self, descriptor: Identifier) -> None:
        """
        Delete my value
        """
        # remove {descriptor} from my inventory
        del self.pyre_identifiers[descriptor.pyre_name]
        # and done
        return

    def pyre_identify(self, authority: typing.Any, **kwds) -> typing.Any:
        """
        Let {authority} know i am a group
        """
        # attempt to
        try:
            # ask {authority} for my handler
            handler = authority.pyre_onGroup
        # if it doesn't understand
        except AttributeError:
            # chain up
            return super().pyre_identify(authority=authority, **kwds)
        # otherwise, invoke the handler
        return handler(group=self, **kwds)

    # implementation details
    @classmethod
    def pyre_newInventory(cls) -> Inventory:
        """
        Build the inventory of a new instance
        """
        # start fresh
        inventory = Inventory()
        # go through all known identifiers
        for name, descriptor in cls.pyre_identifiers.items():
            # clone the descriptor; the cloning is necessary to support adding content to
            # subgroups without modifying the static structure
            clone = descriptor.pyre_clone()
            # register the clone and move to the next one
            inventory[name] = clone
        # all done
        return inventory


# end of file
