# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
import datetime
import json
import uuid

# superclass
from ..standard import Parameters as standard


# declaration
class Parameters(standard.Parameters):
    """
    The parameters of statements in the postgres dialect, where they differ from standard SQL
    """

    # the types of the values that belong to no column, by the type of the value
    types = {
        **standard.Parameters.types,
        str: "TEXT",
        bytes: "BYTEA",
        uuid.UUID: "UUID",
        dict: "JSONB",
    }

    # the forms the bindings take, by the type of the column
    def _pyre_onJSON(self, schema, value, **kwds):
        """
        Keep a json document
        """
        # as its json text, since the bindings would take a list for an array and text for text
        return json.dumps(value)

    # implementation details
    def _numbered(self, index):
        """
        Render the placeholder of the value at {index}, counting from one
        """
        # postgres numbers its placeholders
        return f"${index}"

    def _cast(self, value):
        """
        Build the type of the placeholder of {value}, a value that belongs to no column
        """
        # a time of day or a moment in time with an offset
        if type(value) in (datetime.time, datetime.datetime) and value.utcoffset() is not None:
            # says so, as its literal does
            return f"{self.types[type(value)]} WITH TIME ZONE"
        # the others are typed as the language types them
        return super()._cast(value=value)


# end of file
