# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# external
import journal
import pyre

# typing
import typing
from .Object import Object
from .Group import Group
from .Dataset import Dataset
from .File import File


# the explorer
class Explorer:
    """
    A visitor that inspects an h5 object and extracts its layout
    """

    # interface
    def visit(self, object: Object) -> typing.Optional[Object._pyre_schema.group]:
        """
        Visit the given {file} and extract its layout
        """
        # ask {object} to identify itself and delegate to my handlers
        return object._pyre_identify(authority=self)

        return root

    # visitor implementation
    def _pyre_onFile(self, file: File, **kwds):
        """
        Process a {file}
        """
        # get the underlying h5 object and ask it about the group at the root
        origin = file._pyre_id.group(path="/")
        # form the starting point of the layout
        root = file._pyre_root()
        # and explore it
        return root._pyre_identify(authority=self, hid=origin)

    def _pyre_onGroup(self, group: Group, hid: pyre.libh5.Group, **kwds):
        """
        Process a {group}
        """
        # get the descriptor factoriess
        schema = File._pyre_schema
        # and the low level object types enums
        typeinfo = pyre.libh5.ObjectType
        # go through the group members
        for name, type in hid.members():
            # on groups
            if type == typeinfo.group:
                # make a group with the given {name}
                spec = schema.group(name=name)
                # attach it
                setattr(group, name, spec)
                # explore it
                spec._pyre_identify(authority=self, hid=hid.group(path=name))
                # and move on
                continue
            # on datasets
            if type == typeinfo.dataset:
                # get the underlying dataset object
                dataset = hid.dataset(path=name)
                # inspect it to make a dataset spec
                spec = schema.dataset._pyre_deduce(
                    name=name, cell=dataset.cell, info=dataset.type, shape=dataset.shape
                )
                # attach it to the group being explored
                setattr(group, name, spec)
                # and move on
                continue
        # all done
        return group


# end of file
