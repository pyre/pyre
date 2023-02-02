# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# external
import journal

# superclass
from .Object import Object

# typing
import collections.abc
import typing
from .. import schema
from .Dataset import Dataset


# a basic h5 object
class Group(Object):
    """
    A container of h5 objects
    """

    # metamethods
    def __init__(self, layout: typing.Optional[schema.group] = None, **kwds):
        # chain  up
        super().__init__(layout=layout, **kwds)
        # figure out my layout
        descriptors = layout._pyre_descriptors if layout is not None else {}
        # attach them
        self._pyre_descriptors = descriptors
        # go through them
        for name, descriptor in descriptors.items():
            # and populate my state
            setattr(self, name, descriptor)
        # all done
        return

    # attribute access
    def __getattribute__(self, name: str) -> typing.Any:
        """
        Trap attribute read access unconditionally
        """
        # if the {name} is in the protected namespace
        if name.startswith("_"):
            # do a normal lookup
            return super().__getattribute__(name)
        # otherwise, grab my layout
        descriptors = super().__getattribute__("_pyre_descriptors")
        # attempt to
        try:
            # search for a descriptor associated with this name
            descriptor = descriptors[name]
        # if this fails
        except KeyError:
            # chain up to do a normal attribute lookup
            return super().__getattribute__(name)
        # if it succeeds, {name} is one of ours; attempt to
        try:
            # grab its value
            proxy = super().__getattribute__(name)
        # if this fails
        except AttributeError:
            # we have some work to do
            pass
        # otherwise
        else:
            # if it's a dataset
            if isinstance(proxy, Dataset):
                # grab its value and return it
                return proxy.value
            # otherwise, return it unchanged
            return proxy
        # if we get this far, we know that {name} corresponds to a {descriptor} that
        # doesn't have an actual value yet; compute the location of the member
        location = self._pyre_location / descriptor._pyre_name
        # if the descriptor is a dataset
        if isinstance(descriptor, schema.dataset):
            # make a dataset
            dataset = Dataset(at=location, layout=descriptor)
            # record it
            super().__setattr__(name, dataset)
            # and return its value
            return dataset.value
        # if the descriptor is a group
        if isinstance(descriptor, schema.group):
            # make a group
            group = Group(at=location, layout=descriptor)
            # record it
            super().__setattr__(name, group)
            # and return it
            return group
        # otherwise, we are out of ideas; almost certainly this is a bug caused
        # by the introduction of a new descriptor type that is not handled
        # correctly
        channel = journal.firewall("pyre.h5.api")
        # so build a report
        channel.line(f"unknown descriptor type")
        channel.line(f"{descriptor}")
        channel.line(f"while looking up '{name}' in {self}")
        # complain
        channel.log()
        # and bail, just in case firewalls aren't fatal
        return

    def __setattr__(self, name: str, value: typing.Any) -> None:
        # if the name is in the protected namespace
        if name.startswith("_"):
            # chain up to handle a normal assignment
            return super().__setattr__(name, value)
        # get my descriptors
        descriptors = self._pyre_descriptors
        # if {value} is a layout
        if isinstance(value, schema.descriptor):
            # record it in my layout
            descriptors[name] = value
            # compute the location of the new member
            location = self._pyre_location / value._pyre_name
            # if it's group
            if isinstance(value, schema.group):
                # we'll make a group
                factory = Group
            # if it's a dataset
            elif isinstance(value, schema.dataset):
                # we'll make a dataset
                factory = Dataset
            # anything else
            else:
                # we have a bug, probably caused by the introduction of a new descriptor type
                # that is not handled here
                channel = journal.firewall("pyre.h5.api")
                # so build a report
                channel.line(f"unknown descriptor type")
                channel.line(f"{descriptor}")
                channel.line(f"while looking up '{name}' in {self}")
                # complain
                channel.log()
                # and bail, just in case firewalls aren't fatal
                return
            # make the value
            attr = factory(at=location, layout=value)
            # and set it
            return super().__setattr__(name, attr)
        # if {value} is an h5 element
        if isinstance(value, Object):
            # save its layout
            descriptors[name] = value._pyre_layout
            # and record it
            return super().__setattr__(name, value)
        # if we get this far, {value} is not special; is {name} special? attempt to
        try:
            # lookup a descriptor by this {name}
            descriptor = descriptors[name]
        # if this fails
        except KeyError:
            # nothing is special; process a regular assignment
            return super().__setattr__(name, value)
        # the only remaining legal assignment is to the value of a dataset
        if isinstance(descriptor, schema.dataset):
            # attempt to
            try:
                # get the dataset
                dataset = super().__getattribute__(name)
            # if there isn't one yet
            except AttributeError:
                # compute the location of the new member
                location = self._pyre_location / descriptor._pyre_name
                # make it
                dataset = Dataset(at=location, layout=descriptor)
                # and store it
                super().__setattr__(name, dataset)
            # set its value
            dataset.value = value
            # and done
            return
        # anything else is a bug
        channel = journal.firewall("pyre.h5.api")
        # so build a report
        channel.line(f"cannot assign '{value}'")
        channel.line(f"to '{name}'")
        channel.line(f"associated with {descriptor}")
        channel.line(f"in {self}")
        # complain
        channel.log()
        # and bail, just in case firewalls aren't fatal
        return

    # representation
    def __str__(self):
        """
        Build a human readable representation
        """
        # easy enough
        return f"group '{self._pyre_location}'"

    # framework hooks
    # classifications
    def _pyre_datasets(self) -> collections.abc.Generator:
        """
        Generate a sequence of my datasets
        """
        # hand off
        yield from (
            # descriptor names
            name
            # from the pile of known descriptors
            for name, descriptor in self._pyre_descriptors.items()
            # if they are datasets
            if isinstance(descriptor, schema.dataset)
        )
        # all sone
        return

    def _pyre_groups(self) -> collections.abc.Generator:
        """
        Generate a sequence of my subgroups
        """
        # hand off
        yield from (
            # descriptor names
            name
            # from the pile of known descriptors
            for name, descriptor in self._pyre_descriptors.items()
            # if they are groups
            if isinstance(descriptor, schema.group)
        )
        # all done
        return

    def _pyre_locations(self) -> collections.abc.Generator:
        """
        Generate a sequence of contents
        """
        # every descriptor i know of counts as a location
        yield from self._pyre_descriptors
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


# end of file
