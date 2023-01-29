# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# external
import itertools
import journal
import pyre

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
    def pyre_locate(
        self, location: pyre.primitives.pathlike
    ) -> typing.Optional[Object]:
        """
        Locate the object at the given {location}
        """
        # coerce the location into a path
        location = pyre.primitives.path(location)
        # starting with me
        cursor = self
        # go through the location parts
        for name in location.parts:
            # attempt to
            try:
                # locate the group member
                cursor = cursor.pyre_identifiers[name]
            # if this fails
            except KeyError:
                # make a channel
                channel = journal.error("pyre.h5.group")
                # build the report
                channel.line(f"could not find '{location}'")
                channel.line(f"within the group at '{self.pyre_location}'")
                channel.line(f"'{cursor.pyre_location}' has no member '{name}")
                # and complain
                channel.log()
                # and bail, just in case errors aren't fatal
                return None

        # if all went well, we have found the location
        return cursor

    # access to contents by category
    def pyre_datasets(self) -> typing.Sequence[Dataset]:
        """
        Generate a sequence of my datasets
        """
        # select datasets
        yield from filter(lambda loc: issubclass(loc, Dataset), self.pyre_locations())
        # all done
        return

    def pyre_groups(self) -> typing.Sequence["Group"]:
        """
        Generate a sequence of my subgroups
        """
        # select groups
        yield from filter(lambda loc: issubclass(loc, Group), self.pyre_locations())
        # all done
        return

    def pyre_locations(self) -> typing.Sequence[Location]:
        """
        Generate a sequence of contents
        """
        # hand off all known identifiers
        yield from self.pyre_identifiers.values()
        # all done
        return

    # metamethods
    def __init__(self, identifiers=None, **kwds):
        # chain up
        super().__init__(**kwds)
        # initialize my inventory
        self.pyre_identifiers: Inventory = self.pyre_newInventory(
            identifiers=identifiers
        )
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
            value = self.pyre_get(name=name)
        # if not
        except KeyError:
            # i'm out of ideas
            raise AttributeError(
                f"group '{self.pyre_name}' has no identifier named '{name}'"
            )
        # otherwise, hand it off
        return value

    def __setattr__(self, name: str, value: typing.Any) -> None:
        """
        Trap attribute assignment unconditionally
        """
        # N.B.: unconditionally means _unconditionally_:
        # this gets called during construction, while the objet layout is being initialized;
        # so, during instantiation when my attributes are being initialized
        if name.startswith("pyre_"):
            # stay out of the way
            return super().__setattr__(name, value)
        # get my identifiers
        identifiers = self.pyre_identifiers
        # if {name} is a known identifier or {value} is one of ours
        if name in identifiers or isinstance(value, Object):
            # make structural assignment
            return self.pyre_set(name=name, value=value)
        # everything else is a normal assignment
        return super().__setattr__(name, value)

    def __str__(self) -> str:
        """
        Human readable description
        """
        # say something simple, for now
        return f"group '{self.pyre_name}' at '{self.pyre_location}'"

    # framework hooks
    # content access dispatchers
    def pyre_new(self, name: str, identifier: Identifier):
        """
        Add {identifier} to my content under {name}
        """
        # easy enough
        self.pyre_identifiers[name] = identifier
        # and done
        return

    def pyre_get(self, name: str) -> typing.Any:
        """
        Look up the identifier associated this {descriptor}
        """
        # look up the {identifier} that corresponds to this descriptor
        identifier = self.pyre_identifiers[name]
        # if it is a dataset
        if isinstance(identifier, Dataset):
            # return whatever it provides
            return identifier.value
        # otherwise, grant access to the identifier
        return identifier

    def pyre_set(self, name: str, value: typing.Any) -> None:
        """
        Associate my {descriptor} with {identifier}
        """
        # get my identifiers
        identifiers = self.pyre_identifiers
        # attempt to
        try:
            # look up the {identifier} that corresponds to this descriptor
            identifier = identifiers[name]
        # if it's not there
        except KeyError:
            # make a new assignment
            identifiers[name] = value
            # and move on
            return
        # if it is a dataset
        if isinstance(identifier, Dataset):
            # set its value
            identifier.value = value
            # and done
            return
        # otherwise, override my content with the new identifier
        identifiers[name] = value
        # all done
        return

    def pyre_delete(self, name: str) -> None:
        """
        Delete my value
        """
        # remove {descriptor} from my inventory
        del self.pyre_identifiers[name]
        # and done
        return

    # cloning
    def pyre_clone(self, **kwds):
        """
        # Make as faithful a copy of me as possible
        """
        # chain up with my contents
        return super().pyre_clone(identifiers=self.pyre_identifiers, **kwds)

    # visiting
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
    def pyre_newInventory(cls, identifiers=None) -> Inventory:
        """
        Build the inventory of a new instance
        """
        # start fresh
        inventory = Inventory()
        # if there's no dynamic content
        if identifiers is None:
            # use my static content
            content = cls.pyre_identifiers.items()
        # otherwise
        else:
            # chain my dynamic and static contents
            content = itertools.chain(identifiers.items(), cls.pyre_identifiers.items())
        # go through it
        for name, descriptor in content:
            # if the name is already present
            if name in inventory:
                # skip it; it is being shadowed
                continue
            # otherwise, clone the descriptor and register it; the cloning is necessary
            # to support adding content to subgroups without modifying any existing structure
            inventory[name] = descriptor.pyre_clone()
        # all done
        return inventory


# end of file
