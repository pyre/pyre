# -*- coding: utf-8 -*-


# superclass
from .File import File


# the base reader
class Reader(File):
    """
    The base reader for h5 products
    """


    # interface
    def open(self, path):
        """
        Access the h5 file at {path}
        """
        # set the mode and delegate
        return super().open(path=path, mode="r")


    def read(self, query=None):
        """
        Open the h5 file at {path} and read the information in {query}
        """
        # if the user doesn't have any opinions
        if query is None:
            # grab my schema and use it for guidance as to what to read from the file
            query = self.schema()

        # visit the {query} structure and return the result
        return query.pyre_identify(authority=self)


    # implementation details
    def pyre_onDataset(self, dataset, parent=None):
        """
        Process a {group} at {prefix}
        """
        # clone
        clone = dataset.pyre_clone()
        # if i have a known parent
        if parent:
            # attach me
            parent.pyre_set(descriptor=clone, value=clone)
        # all done
        return clone


    def pyre_onGroup(self, group, parent=None):
        """
        Process a {group}
        """
        # clone
        clone = group.pyre_clone()
        # if i have a known parent
        if parent:
            # attach me
            parent.pyre_set(descriptor=clone, value=clone)
        # go through my children
        for child in group.pyre_locations():
            # and visit each one
            child.pyre_identify(authority=self, parent=clone)
        # all done
        return clone


# end of file
