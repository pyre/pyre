# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# support
import pyre

# superclass
from .Object import Object

# typing
import typing
import collections.abc
from .. import libh5
from .Dataset import Dataset

# type aliases
H5ObjectType = libh5.ObjectType


# a basic h5 object
class Group(Object):
    """
    A container of h5 objects
    """

    # metamethods
    def __init__(
        self,
        at: typing.Optional[pyre.primitives.pathlike] = "/",
        **kwds,
    ):
        # chain  up
        super().__init__(at=at, **kwds)
        # initialize my members
        self._pyre_contents = set()
        # all done
        return

    # attribute access
    def __getattribute__(self, name: str) -> typing.Any:
        """
        Look up {name}
        """
        # get the value
        member = super().__getattribute__(name)
        # if it is a dataset
        if isinstance(member, Dataset):
            # grab its value and return it
            return member.value
        # otherwise, just return the member itself
        return member

    def __setattr__(self, name: str, value: typing.Any) -> None:
        # if the {name} is already registered
        if hasattr(self, name):
            # get the object
            member = super().__getattribute__(name)
            # if it is a dataset
            if isinstance(member, Dataset):
                # set its value
                member.value = value
                # and do no more
                return
        # if {value} is an hdf5 object
        if isinstance(value, Object):
            # record it
            self._pyre_contents.add(name)
        # and make a normal assignment
        return super().__setattr__(name, value)

    def __delattr__(self, name: str) -> None:
        # forget {name}
        self._pyre_contents.discard(name)
        # and chain up to remove the attribute
        return super().__delattr__(name)

    # member access
    def __getitem__(self, path):
        """
        Lookup {path} within my subtree
        """
        # delegate
        return self._pyre_find(path=path)

    # representation
    def __str__(self):
        """
        Build a human readable representation
        """
        # easy enough
        return f"group '{self._pyre_location}'"

    # framework hooks
    # directed traversal
    def _pyre_descriptor(self, path: pyre.primitives.pathlike) -> Object:
        """
        Look up the h5 object associated with {path} within the subtree managed by this
        group, assuming it is already bound to a live h5 object
        """
        # normalize path
        path = pyre.primitives.path(path)
        # start the search with me
        cursor = self
        # go through the path parts
        for fragment in path.names:
            # translate the path {fragment} into an attribute name
            name = cursor._pyre_layout._pyre_aliases[fragment]
            # find the child, carefully bypassing the forced dataset evaluation
            # so we can hunt down the object and not its value
            cursor = super(Group, cursor).__getattribute__(name)
        # all done
        return cursor

    def _pyre_find(self, path: pyre.primitives.pathlike) -> typing.Any:
        """
        Look up the h5 {object} associated with {path} within the subtree managed by this
        group, assuming it is already bound to a live h5 object
        """
        # normalize path
        path = pyre.primitives.path(path)
        # start the search with me
        cursor = self
        # go through the path parts
        for fragment in path.names:
            # translate the path {fragment} into an attribute name
            name = cursor._pyre_layout._pyre_aliases[fragment]
            # point to the new child and move on
            cursor = getattr(cursor, name)
        # all done
        return cursor

    # classifications
    def _pyre_datasets(self) -> collections.abc.Generator:
        """
        Generate a sequence of my datasets
        """
        # go through my locations
        for location in self._pyre_locations():
            # identify the ones that are datasets
            if isinstance(location, Dataset):
                # hand it off
                yield location
        # all done
        return

    def _pyre_groups(self) -> collections.abc.Generator:
        """
        Generate a sequence of my subgroups
        """
        # go through my locations
        for location in self._pyre_locations():
            # identify the ones that are groups
            if isinstance(location, Group):
                # hand it off
                yield location
        # all done
        return

    def _pyre_locations(self) -> collections.abc.Generator:
        """
        Generate a sequence of contents
        """
        # go through the known descriptors
        for member in self._pyre_contents:
            # look up the corresponding location
            location = super().__getattribute__(member)
            # and hand it off
            yield location
        # all done
        return

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

    # the inspector gets patched by the module initializer
    _pyre_inspector = None


# end of file
