# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# support
import journal
import pyre

# superclass
from .Object import Object

# typing
import collections.abc
import typing
from .Dataset import Dataset


# a basic h5 object
class Group(Object):
    """
    A container of h5 objects
    """

    # types
    _pyre_objectTypes = pyre.libh5.ObjectType

    # metamethods
    def __init__(
        self, layout: typing.Optional[Object._pyre_schema.group] = None, **kwds
    ):
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
        if isinstance(descriptor, self._pyre_schema.dataset):
            # make a dataset
            dataset = Dataset(at=location, layout=descriptor)
            # record it
            super().__setattr__(name, dataset)
            # and return its value
            return dataset.value
        # if the descriptor is a group
        if isinstance(descriptor, self._pyre_schema.group):
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
        if isinstance(value, self._pyre_schema.descriptor):
            # record it in my layout
            descriptors[name] = value
            # compute the location of the new member
            location = self._pyre_location / value._pyre_name
            # if it's group
            if isinstance(value, self._pyre_schema.group):
                # we'll make a group
                factory = Group
            # if it's a dataset
            elif isinstance(value, self._pyre_schema.dataset):
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
        if isinstance(descriptor, self._pyre_schema.dataset):
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
    def _pyre_find(self, path: pyre.primitives.pathlike) -> typing.Optional[Object]:
        """
        Look up the h5 {object} associated with {path} within the subtree managed by this
        group, assuming it is already bound to a live h5 object
        """
        # pull the object type enums
        objectTypes = self._pyre_objectTypes
        # and the schema
        schema = self._pyre_schema
        # grab the low level object
        hid, info = self._pyre_id.get(str(path))
        # compute the location of the member
        location = self._pyre_location / path
        # extract the name of the node
        name = location.name
        # on groups
        if info == objectTypes.group:
            # build the layout
            layout = schema.group(name=name)
            # build the node
            group = Group(id=hid, at=location, layout=layout)
            # and return it
            return group
        # on datasets
        if info == objectTypes.dataset:
            # build the layout
            layout = schema.dataset._pyre_deduce(
                name=name, cell=hid.cell, info=hid.type, shape=hid.shape
            )
            # build the node
            dataset = Dataset(id=hid, at=location, layout=layout)
            # and return it
            return dataset
        # anything else implies an objet type that we do not support currently
        channel = journal.firewall("pyre.h5.group")
        # make a report
        channel.line(f"unsupported member type {info.name}")
        channel.line(f"while looking up {path}")
        channel.line(f"in {self}")
        # complain
        channel.log()
        # and bail, just in case firewalls aren't fatal
        return

    # classifications
    def _pyre_datasets(self) -> collections.abc.Generator:
        """
        Generate a sequence of my datasets
        """
        # go through the known descriptors
        for name, descriptor in self._pyre_descriptors.items():
            # identify the ones that are groups
            if isinstance(descriptor, self._pyre_schema.dataset):
                # look up the corresponding dataset; carefully so we don't cause the
                # evaluation we force by default
                dataset = super().__getattribute__(name)
                # and hand off the pair
                yield (name, dataset)
        # all done
        return

    def _pyre_groups(self) -> collections.abc.Generator:
        """
        Generate a sequence of my subgroups
        """
        # go through the known descriptors
        for name, descriptor in self._pyre_descriptors.items():
            # identify the ones that are groups
            if isinstance(descriptor, self._pyre_schema.group):
                # look up the corresponding group
                group = super().__getattribute__(name)
                # and hand off the pair
                yield (name, group)
        # all done
        return

    def _pyre_locations(self) -> collections.abc.Generator:
        """
        Generate a sequence of contents
        """
        # go through the known descriptors
        for name in self._pyre_descriptors:
            # look up the corresponding location
            location = super().__getattribute__(name)
            # and hand off the pair
            yield (name, location)
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
