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
        return query.pyre_identify(authority=self, parent=file, uri=uri, path=root)

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
        path: pyre.primitives.pathlike,
        **kwds,
    ) -> Dataset:
        """
        Process a {group} at {prefix}
        """
        # get the dataset key
        location = str(dataset.pyre_location)
        # use it to update the current path
        path /= location
        # attempt to
        try:
            # realize the h5 object that gives me access to my contents
            hid = parent.pyre_id.dataset(path=location)
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
        # otherwise, clone the {dataset}
        clone = dataset.pyre_clone(id=hid)
        # and attempt to
        try:
            # pull the value
            clone.pyre_read()
        # if anything goes wrong
        except Exception as error:
            # make a channel
            channel = journal.error("pyre.h5.reader")
            # let the user know
            channel.line(f"error: {error}")
            channel.line(f"while reading '{path}'")
            channel.line(f"in '{uri}'")
            # flush
            channel.log()
            # and bail
            raise

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
        path: pyre.primitives.pathlike,
        **kwds,
    ) -> Group:
        """
        Process a {group}
        """
        # get the group location
        location = group.pyre_location
        # update the current path
        path /= location
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
        clone = group.pyre_clone(id=hid)
        # attach the clone to its parent; use the {group} from the query as the descriptor
        # in order to minimize the number of objects with {libh5} footprint
        parent.pyre_set(descriptor=group, identifier=clone)

        # now, go through its children
        for child in group.pyre_locations():
            # and visit each one
            child.pyre_identify(
                authority=self, parent=clone, uri=uri, path=path, **kwds
            )
        # all done
        return parent


# end of file
