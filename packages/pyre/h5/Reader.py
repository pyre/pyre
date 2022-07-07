# -*- coding: utf-8 -*-


# parts
from .File import File

# typing
import pyre
from .Dataset import Dataset
from .Group import Group
from .Location import Location


# the base reader
class Reader:
    """
    The base reader for h5 products
    """

    # interface
    def read(self, path: pyre.primitives.pathlike, query: Location = None) -> Location:
        """
        Open the h5 file at {path} and read the information in {query}
        """
        # create the top level container
        file = File().open(path=path, mode="r")
        # if the user doesn't have any opinions
        if query is None:
            # grab my schema and use it for guidance as to what to read from the file
            query = self.schema()
        # visit the {query} structure and return the result; the initial {parent} is the {file}
        # object, therefore {query} must be anchored by an element whose {pyre_location} is a
        # valid absolute path
        return query.pyre_identify(authority=self, parent=file)

    # implementation details
    def schema(self):
        """
        Retrieve the schema of the data product
        """
        # i don't have one; force subclasses to define
        raise NotImplementedError(
            f"class '{type(self).__name__}' must implement 'schema'"
        )

    # structure traversal
    def pyre_onDataset(self, dataset: Dataset, parent: Group) -> Dataset:
        """
        Process a {group} at {prefix}
        """
        # realize the h5 object that gives me access to my contents
        hid = parent.pyre_id.dataset(path=str(dataset.pyre_location))
        # clone the {dataset}
        clone = dataset.pyre_clone(id=hid)
        # attach the clone to its parent; use the {dataset} from the query as the descriptor
        # in order to minimize the number of objects with {libh5} footprint
        parent.pyre_set(descriptor=dataset, identifier=clone)
        # all done
        return parent

    def pyre_onGroup(self, group: Group, parent: Group) -> Group:
        """
        Process a {group}
        """
        # realize the h5 object that gives me access to the group contents
        hid = parent.pyre_id.group(path=str(group.pyre_location))
        # clone it
        clone = group.pyre_clone(id=hid)
        # attach the clone to its parent; use the {group} from the query as the descriptor
        # in order to minimize the number of objects with {libh5} footprint
        parent.pyre_set(descriptor=group, identifier=clone)
        # now, go through its children
        for child in group.pyre_locations():
            # and visit each one
            child.pyre_identify(authority=self, parent=clone)
        # all done
        return parent


# end of file
