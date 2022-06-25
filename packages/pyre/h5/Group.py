#-*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2022 all rights reserved


# external
import itertools
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
class Group(Object):
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
    def pyre_extend(self, identifier: Identifier) -> 'Group':
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


    def pyre_groups(self) -> typing.Sequence['Group']:
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
        # - the static layout of my {mro}, with each superclass contributing the identifiers it
        #    declares; stored by {schema} in {pyre_identifiers}
        # - the pile of identifiers added programmatically; stored in {pyre_identifiers}
        #
        # collating identifiers from these sources requires taking shadowing into account
        # shadowing is determined by the {pyre_location} of an identifier, not its {pyre_name}
        # inconsistencies caused by decorrelations between names and locations are considered bugs

        # make a pile of identifier names that have been encountered
        known = set()
        # get the full sequence of identifiers
        identifiers = itertools.chain(
            # the identifiers added at runtime
            self.pyre_identifiers.values(),
            # the identifiers from my static structure
            *(base.pyre_identifiers.values()
                for base in type(self).mro() if hasattr(base, "pyre_identifiers"))
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
        self.pyre_inventory: Inventory = Inventory()
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
            raise AttributeError(f"group '{self.pyre_name}' has no identifier named '{name}'")

        # otherwise, ask it to do its thing
        return identifier.__get__(instance=self, cls=type(self))


    def __setattr__(self, name: str, value: typing.Any) -> None:
        """
        Trap attribute assignment to support dynamic identifiers
        """
        # check whether
        try:
            # {name} points to one of my dynamic identifiers
            identifier = self.pyre_identifiers[name]
        # if not
        except KeyError:
            # delegate
            return super().__setattr__(name, value)

        # if it is, ask it to do its thing
        return identifier.__set__(instance=self, value=value)


    def __str__(self) -> str:
        """
        Human readable description
        """
        # say something simple, for now
        return f"group '{self.pyre_name}' at '{self.pyre_location}'"


    # framework hooks
    def pyre_get(self, descriptor: Identifier) -> typing.Any:
        """
        Read my value
        """
        # attempt to
        try:
            # get the {descriptor} value from my {inventory}
            value = self.pyre_inventory[descriptor.pyre_name]
        # if i don't have an explicit value for {descriptor} yet
        except KeyError:
            # ask for a refresh
            value = descriptor.pyre_sync(instance=self)
        # and return it
        return value


    def pyre_set(self, descriptor: Identifier, value: typing.Any) -> None:
        """
        Write my value
        """
        # update the value of {descriptor} in my {inventory}
        self.pyre_inventory[descriptor.pyre_name] = value
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


    def pyre_sync(self, instance: 'Group', **kwds) -> 'Group':
        """
        Hook invoked when the {inventory} lookup fails and a value must be generated
        """
        # build a clone of mine to hold my client's values for my structure
        group = type(self)(name=self.pyre_name, at=self.pyre_location)
        # make sure {instance} remembers my clone; this step is important for groups so that
        # {instance} local storage is created to support further content access
        # there is a test case that checks for this...
        instance.pyre_set(descriptor=self, value=group)
        # and return it
        return group


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


# end of file
