# -*- coding: utf-8 -*-


# support
import journal

# superclass
from .File import File

# typing
import os
from .Dataset import Dataset
from .Group import Group
from .Location import Location


# the base reader
class Reader(File):
    """
    The base reader for h5 products
    """

    # interface
    def open(self, path: os.PathLike) -> File:
        """
        Access the h5 file at {path}
        """
        # set the mode and delegate
        return super().open(path=path, mode="r")

    def read(self, query: Location = None) -> Location:
        """
        Open the h5 file at {path} and read the information in {query}
        """
        # if the user doesn't have any opinions
        if query is None:
            # grab my schema and use it for guidance as to what to read from the file
            query = self.schema()
        # visit the {query} structure and return the result; the initial {parent} is the {file}
        # object, therefore {query} must be anchored by an element whose {pyre_location} is a
        # valid absolute path
        return query.pyre_identify(authority=self, parent=self)

    # implementation details
    def pyre_onDataset(self, dataset: Dataset, parent: Group) -> Dataset:
        """
        Process a {group} at {prefix}
        """
        # realize the h5 object that gives me access to my contents
        hid = parent.pyre_id.dataset(path=str(dataset.pyre_location))
        # clone the {dataset}
        clone = dataset.pyre_clone(id=hid)
        # attach the clone to its parent
        parent.pyre_set(descriptor=clone, identifier=clone)
        # all done
        return clone

    def pyre_onGroup(self, group: Group, parent: Group) -> Group:
        """
        Process a {group}
        """
        # realize the h5 object that gives me access to the group contents
        hid = parent.pyre_id.group(path=str(group.pyre_location))
        # clone it
        clone = group.pyre_clone(id=hid)
        # attach it to its parent
        parent.pyre_set(descriptor=clone, identifier=clone)
        # now, go through its children
        for child in group.pyre_locations():
            # and visit each one
            child.pyre_identify(authority=self, parent=clone)
        # all done
        return clone


# end of file
