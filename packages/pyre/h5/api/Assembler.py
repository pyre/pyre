# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


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
    def _pyre_onGroup(self, group: schema.group, parent: typing.Optional[Group] = None) -> Group:
        """
        Process a {group}
        """
        # if i don't have a parent
        if parent is None:
            # i'm building the root node; it mounts at its declared location, if any
            mount = group._pyre_location
            # otherwise at the file root
            location = pyre.primitives.path(mount) if mount else pyre.primitives.path.root
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
        # if i am not the root of this assembly
        if parent is not None:
            # my parent takes it from here
            return node
        # otherwise, realize my ancestry as well, so that the tree can be navigated from
        # the file root down, and hand off whatever sits at the top
        return self._pyre_mount(node=node, location=location)

    # implementation details
    def _pyre_mount(self, node: Group, location: pyre.primitives.path) -> Group:
        """
        Realize the groups from the file root down to {node}, which mounts at {location},
        and return the top of the chain
        """
        # the names of my ancestors, from the file root down
        ancestry = list(location.parent.names)
        # a product that mounts at the file root has no ancestry
        if not ancestry:
            # so it is its own top
            return node
        # otherwise, start the chain with the file root
        top = Group(at=pyre.primitives.path.root, layout=schema.group(name="/"))
        # which is where the descent begins
        cursor = top
        # along with the path we accumulate as we go
        at = pyre.primitives.path.root
        # go through my ancestors
        for name in ancestry:
            # extend the path
            at = at / name
            # make a group there; ancestors are pure structure, so a bare layout is enough
            child = Group(at=at, layout=schema.group(name=name))
            # attach it to the one above, teaching it how to translate the path fragment
            self._pyre_attach(parent=cursor, child=child, name=name)
            # and descend
            cursor = child
        # finally, hang the mounted node off the deepest ancestor
        self._pyre_attach(parent=cursor, child=node, name=location.name)
        # and hand off the top of the chain
        return top

    @staticmethod
    def _pyre_attach(parent: Group, child: Group, name: str) -> None:
        """
        Make {child} a member of {parent} under the given {name}
        """
        # register the name with the parent's layout, so that path based lookups can
        # translate this fragment into an attribute name
        parent._pyre_layout._pyre_aliases[name] = name
        # and place the child within reach of attribute access
        setattr(parent, name, child)
        # all done
        return

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
