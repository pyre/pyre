# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# external
import pyre

# superclass
from .Inspector import Inspector

# typing
import typing
from .. import libh5
from .. import schema
from .Object import Object
from .Dataset import Dataset
from .Group import Group
from .File import File

# type aliases
H5Group = libh5.Group
H5DataSet = libh5.DataSet
H5Object = typing.Union[H5Group, H5DataSet]
H5ObjectType = libh5.ObjectType


# the explorer
class Explorer(Inspector):
    """
    A visitor that builds the layout of an h5 object by examining its on-disk content
    """

    # interface
    def visit(self, object: Object) -> schema.descriptor:
        """
        Visit the given {file} and extract its layout
        """
        # ask {object} to identify itself and delegate to my handlers
        return object._pyre_identify(authority=self)

    # visitor implementation
    def _pyre_onFile(self, file: File) -> schema.group:
        """
        Build a descriptor for the given {group}
        """
        # get the {file} handle
        h5id = file._pyre_id
        # build a group descriptor and return it
        return self._pyre_inferGroupDescriptor(name="root", h5id=h5id)

    def _pyre_onGroup(self, group: Group) -> schema.group:
        """
        Build a descriptor for the given {group}
        """
        # get the {group} handle
        h5id = group._pyre_id
        # and its name
        name = group._pyre_location.name
        # build a group descriptor and return it
        return self._pyre_inferGroupDescriptor(name=name, h5id=h5id)

    def _pyre_onDataset(self, dataset: Dataset) -> schema.dataset:
        """
        Build a type descriptor for the given {dataset}
        """
        # get the dataset handle
        h5id = dataset._pyre_id
        # and its entry name in its group
        name = dataset._pyre_location.name
        # build a type descriptor and return it
        return self._pyre_inferDatasetDescriptor(name=name, h5id=h5id)


# end of file
