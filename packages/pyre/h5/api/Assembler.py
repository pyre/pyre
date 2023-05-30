# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# external
import pyre

# get the schema
from .. import schema

# and the local concrete nodes
from .Object import Object
from .Group import Group
from .Dataset import Dataset

# typing
import typing


# give shape to a schema
class Assembler:
    """
    A {schema} visitor that shapes the structure of an h5 file
    """

    # interface
    def visit(self, descriptor: schema.descriptor) -> Object:
        """
        Build the concrete h5 entity that corresponds to the given {descriptor}
        """
        # delegate to the correct handler
        return descriptor._pyre_identify(authority=self)

    # framework hooks
    def _pyre_onGroup(
        self, group: schema.group, parent: typing.Optional[Group] = None
    ) -> Group:
        """
        Process a {group}
        """
        # if i don't have a parent
        if parent is None:
            # i'm building the root node
            location = pyre.primitives.path.root
        # otherwise
        else:
            # splice the {group} name to my parent's location
            location = parent._pyre_location / group._pyre_name
        # build the group
        node = Group(at=location, layout=group)
        # go through the {group} contents
        for descriptor in group._pyre_descriptors():
            # look up its attribute name
            name = group._pyre_aliases[descriptor._pyre_name]
            # assemble the {child} node
            child = descriptor._pyre_identify(authority=self, parent=node)
            # and attach it to my node
            setattr(node, name, child)
        # all done
        return node

    def _pyre_onDataset(self, dataset: schema.dataset, parent: Group) -> Dataset:
        """
        Process a {dataset}
        """
        # compute my location
        location = parent._pyre_location / dataset._pyre_name
        # make a dataset
        node = Dataset(at=location, layout=dataset)
        # and return it
        return node


# end pf file
