# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# external
import journal
import pyre

# typing
import typing
from .File import File


# the explorer
class Explorer:
    """
    A visitor that inspects an h5 file and extracts its layout
    """

    # interface
    def visit(self, file: File) -> typing.Optional[File._pyre_schema.group]:
        """
        Visit the given {file} and extract its layout
        """
        # normalize the starting point
        root = file._pyre_root()
        # get the file handle
        handle = file._pyre_id
        # and ask it about the group at the {root}
        origin = handle.group(path="/")
        # look for its structure
        self._explore(layout=root, group=origin)
        # and return it
        return root

    # implementation details
    def _explore(self, layout, group):
        """
        Extract information from {group} and populate {layout}
        """
        # get the descriptors
        schema = File._pyre_schema
        # get the object types
        typeinfo = pyre.libh5.ObjectType
        # go through the members
        for name, type in group.members():
            # on groups
            if type == typeinfo.group:
                # make a group
                descriptor = schema.group(name=name)
                # and adjust my layout
                setattr(layout, name, descriptor)
                # get the h5 object
                hid = group.group(path=name)
                # explore it
                self._explore(layout=descriptor, group=hid)
                # and move on
                continue
            # on dataset
            if type == typeinfo.dataset:
                # get the h5 object
                hid = group.dataset(path=name)
                # make a dataset
                descriptor = schema.dataset._pyre_deduce(
                    name=name, cell=hid.cell, info=hid.type, shape=hid.shape
                )
                # adjust my layout
                setattr(layout, name, descriptor)
                # and move on
                continue

        # all done
        return


# end of file
