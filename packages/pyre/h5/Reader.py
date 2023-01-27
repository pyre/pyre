# -*- coding: utf-8 -*-


# external
import journal

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
    def read(self, uri: pyre.primitives.pathlike, query: Location = None) -> Location:
        """
        Open the h5 file at {path} and read the information in {query}
        """
        # create the top level container
        file = File().open(uri=uri, mode="r")
        # if the user doesn't have any opinions
        if query is None:
            # grab my schema and use it for guidance as to what to read from the file
            query = self.schema()
        # starting at
        root = pyre.primitives.path.root
        # visit the {query} structure and return the result; the initial {parent} is the {file}
        # object, therefore {query} must be anchored by an element whose {pyre_location} is a
        # valid absolute path
        return query.pyre_identify(authority=self, parent=file, uri=uri)

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
    def pyre_onDataset(
        self,
        dataset: Dataset,
        parent: Group,
        uri: pyre.primitives.pathlike,
        **kwds,
    ) -> Group:
        """
        Process a {dataset} at {prefix}
        """
        # get the dataset location
        location = str(dataset.pyre_location)
        # form the path to it
        path = parent.pyre_location / location
        # attempt to
        try:
            # realize the h5 object that gives me access to the dataset contents
            hid = parent.pyre_id.dataset(path=location)
        # if anything goes wrong
        except Exception as error:
            # make a channel
            channel = journal.warning("pyre.h5.reader")
            # let the user know
            channel.line(f"warning: {error}")
            channel.line(f"while looking up '{path}'")
            channel.line(f"in '{uri}'")
            # flush
            channel.log()
            # and move on
            return parent
        # otherwise, clone the {dataset}
        clone = dataset.pyre_clone(id=hid, at=path)
        # and attempt to
        try:
            # pull the value
            clone.pyre_read()
        # if anything goes wrong
        except Exception as error:
            # make a channel
            channel = journal.warning("pyre.h5.reader")
            # let the user know
            channel.line(f"{error}")
            channel.line(f"while attempting to read '{path}'")
            channel.line(f"in '{uri}'")
            # flush
            channel.log()
            # and bail
            return parent
        # attach the clone to its parent; use the {dataset} from the query as the descriptor
        # in order to minimize the number of objects with {libh5} footprint
        parent.pyre_set(descriptor=dataset, identifier=clone)
        # all done
        return parent

    def pyre_onGroup(
        self,
        group: Group,
        parent: Group,
        uri: pyre.primitives.pathlike,
        **kwds,
    ) -> Group:
        """
        Process a {group}
        """
        # get the group location
        location = group.pyre_location
        # form the path to it
        path = parent.pyre_location / location
        # attempt to
        try:
            # realize the h5 object that gives me access to the group contents
            hid = parent.pyre_id.group(path=str(location))
        # if anything goes wrong
        except Exception as error:
            # make a channel
            channel = journal.error("pyre.h5.reader")
            # let the user know
            channel.line(f"error: {error}")
            channel.line(f"while looking up '{path}'")
            channel.line(f"in '{uri}'")
            # flush
            channel.log()
            # and bail
            raise
        # otherwise, clone it
        clone = group.pyre_clone(id=hid, at=path)
        # attach the clone to its parent; use the {group} from the query as the descriptor
        # in order to minimize the number of objects with {libh5} footprint
        parent.pyre_set(descriptor=group, identifier=clone)

        # now, go through its children
        for child in group.pyre_locations():
            # and visit each one
            child.pyre_identify(authority=self, parent=clone, uri=uri, **kwds)
        # all done
        return parent


# end of file
