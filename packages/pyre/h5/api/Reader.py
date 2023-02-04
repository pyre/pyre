# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# external
import journal

# support
from .Explorer import Explorer

# typing
import pyre
import typing
from .. import schema
from .Object import Object
from .File import File


# the reader
class Reader:
    """
    The base reader of h5 data products

    This is a visitor that populates an h5 object from the contents of a file given a {query}
    that describes a subset of the hierarchy
    """

    # interface
    def read(
        self, file: File, query: typing.Optional[schema.group] = None
    ) -> typing.Optional[Object]:
        """
        Read {file} and extract an h5 {object} with the structure of {query}
        """
        # normalize the starting point
        if query is None:
            # get my schema
            query = self.schema(file=file)
        # visit the {query} and populate the {file}
        query._pyre_identify(authority=self, parent=file)
        # find where {query} fits within {file} and return it
        return file

    # implementation details
    def schema(self, file, **kwds) -> schema.group:
        """
        Retrieve the schema of the data product
        """
        # the default is dynamic discovery, implemented by getting an explorer
        explorer = Explorer()
        # to discover the structure of the file
        return explorer.explore(file=file)


# end of file
