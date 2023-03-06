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
        self,
        layout: typing.Optional[Object._pyre_schema.group] = None,
        at: typing.Optional[pyre.primitives.pathlike] = "/",
        **kwds,
    ):
        # chain  up
        super().__init__(layout=layout, at=at, **kwds)
        # initialize my members
        self._pyre_members = set()
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
        # if {value} is an hdf5 object
        if isinstance(value, Object):
            # record it
            self._pyre_members.add(name)
        # and make a normal assignment
        return super().__setattr__(name, value)

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
            # load its value
            dataset.value = layout._pyre_pull(dataset=dataset)
            # and return it
            return dataset
        # anything else implies an object type that we do not support currently
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
        # get my spec
        spec = self._pyre_layout
        # if it's trivial
        if spec is None:
            # nothing further
            return
        # go through my descriptors
        for descriptor in spec._pyre_descriptors():
            # identify the ones that are groups
            if isinstance(descriptor, self._pyre_schema.dataset):
                # get the name
                name = descriptor._pyre_name
                # look up the corresponding dataset; carefully so we don't cause the
                # evaluation we force by default
                dataset = super().__getattribute__(name)
                # and hand it off
                yield dataset
        # all done
        return

    def _pyre_groups(self) -> collections.abc.Generator:
        """
        Generate a sequence of my subgroups
        """
        # get my spec
        spec = self._pyre_layout
        # if it's trivial
        if spec is None:
            # nothing further
            return
        # go through the known descriptors
        for descriptor in spec._pyre_descriptors():
            # identify the ones that are groups
            if isinstance(descriptor, self._pyre_schema.group):
                # get the name
                name = descriptor._pyre_name
                # look up the corresponding group
                group = super().__getattribute__(name)
                # and hand it off
                yield group
        # all done
        return

    def _pyre_locations(self) -> collections.abc.Generator:
        """
        Generate a sequence of contents
        """
        # get my spec
        spec = self._pyre_layout
        # if it's trivial
        if spec is None:
            # nothing further
            return
        # go through the known descriptors
        for descriptor in spec._pyre_descriptors():
            # get the name
            name = descriptor._pyre_name
            # look up the corresponding location
            location = super().__getattribute__(name)
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


# end of file
