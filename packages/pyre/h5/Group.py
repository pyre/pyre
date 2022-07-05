# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2022 all rights reserved


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
    A container of datasets
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
    # add a new identifier
    def pyre_extend(self, identifier: Identifier) -> "Group":
        """
        Add a new {identifier} to this group

        The {identifier} must have a {pyre_name}
        """
        # add it to my pile
        self.pyre_identifiers[identifier.pyre_name] = identifier
        # all done
        return self

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
        # N.B.:
        # currently, there are two possible sources of identifiers in my contents
        # - the static layout of my class; stored in the {pyre_identifiers} class attribute
        # - the pile of identifiers added programmatically; stored in my {pyre_identifiers}
        #
        # collating identifiers from these sources requires taking shadowing into account
        # shadowing is determined by the {pyre_location} of an identifier, not its {pyre_name};
        # inconsistencies caused by decorrelations between names and locations are considered bugs

        # make a pile of identifier names that have been encountered
        known = set()
        # get the full sequence of identifiers
        identifiers = itertools.chain(
            # the identifiers added at runtime
            self.pyre_identifiers.values(),
            # the identifiers from my static structure
            type(self).pyre_identifiers.values(),
        )
        # go through them
        for identifier in identifiers:
            # get their location
            location = identifier.pyre_location
            # if this location is being shadowed
            if location in known:
                # move on
                continue
            # otherwise, add it to the pile of {known} locations
            known.add(location)
            # and send off the {identifier}
            yield identifier
        # all done
        return

    # metamethods
    def __init__(self, **kwds):
        # chain up
        super().__init__(**kwds)
        # initialize my inventory
        self.pyre_inventory: Inventory = self.pyre_newInventory()
        # and my pile of dynamic contents
        self.pyre_identifiers: typing.Dict[str, Identifier] = {}
        # all done
        return

    def __getattr__(self, name: str) -> typing.Any:
        """
        Trap attribute look up to support dynamic identifiers
        """
        # looking up {name} has failed; check whether
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
        # during instantiation
        if name.startswith("pyre_"):
            # stay out of the way
            return super().__setattr__(name, value)
        # if {value} is not an {identifier}
        if not isinstance(value, Identifier):
            # delegate to process a normal assignment
            return super().__setattr__(name, value)
        # if this is an introduction of a new member
        if name not in self.pyre_identifiers:
            # register the newcomer
            self.pyre_identifiers[name] = value
        # add it to my inventory
        self.pyre_inventory[name] = value
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
        Look up the identifier associated the {descriptor} name in my {pyre_inventory}
        """
        # look up the {identifier} that corresponds to this descriptor
        identifier = self.pyre_inventory[descriptor.pyre_name]
        # and return it
        return identifier

    def pyre_set(self, descriptor: Identifier, identifier: Identifier) -> None:
        """
        Associate the {descriptor} name with {identifier} in my {pyre_inventory}
        """
        # update the value of {descriptor} in my {inventory}
        self.pyre_inventory[descriptor.pyre_name] = identifier
        # all done
        return

    def pyre_delete(self, descriptor: Identifier) -> None:
        """
        Delete my value
        """
        # remove {descriptor} from my inventory
        del self.pyre_inventory[descriptor.pyre_name]
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
            # clone the descriptor
            clone = descriptor.pyre_clone()
            # register the clone and move to the next one
            inventory[name] = clone
        # all done
        return inventory


# end of file
