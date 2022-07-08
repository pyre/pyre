# -*- coding: utf-8 -*-


# parts
from .File import File

# typing
import pyre
from .Group import Group


# the base writer
class Writer:
    """
    The base writer for h5 products
    """

    # interface
    def write(self, path: pyre.primitives.pathlike, query: Group, mode="w"):
        """
        Open the h5 file at {path} and write the information in {query}
        """
        # open the file
        file = File().open(path=path, mode=mode)
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


# end of file
