# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# externals
import json

# superclass
from .Schema import Schema


# my declaration
class JSON(Schema):
    """
    A type declarator for json documents: whatever {json.dumps} writes and {json.loads} reads
    """

    # constants
    typename = "json"  # the name of my type
    complaint = "could not coerce {0.value!r} into a json document"  # refusal

    # interface
    def coerce(self, value, **kwds):
        """
        Attempt to convert {value} into a json document
        """
        # text
        if isinstance(value, str):
            # is the json text of a document
            try:
                # so read it
                return json.loads(value)
            # if it is not json
            except ValueError as error:
                # complain, passing along the reason
                raise self.CastingError(value=value, description=self.complaint, error=error)
        # anything else is a document already, as long as json can write it
        try:
            # so try
            json.dumps(value)
        # if it can't
        except (TypeError, ValueError) as error:
            # complain, passing along the reason
            raise self.CastingError(value=value, description=self.complaint, error=error)
        # otherwise, take it as it is
        return value

    def string(self, value):
        """
        Render {value} as a string that can be persisted for later coercion
        """
        # respect {None}
        if value is None:
            # by leaving it alone
            return None
        # the json text of the document
        return json.dumps(value)

    # visiting
    def _pyre_identify(self, authority, **kwds):
        """
        Let {authority} know i am a json document
        """
        # attempt to
        try:
            # ask {authority} for my handler
            handler = authority._pyre_onJSON
        # if it doesn't understand
        except AttributeError:
            # chain up
            return super()._pyre_identify(authority=authority, **kwds)
        # otherwise, invoke the handler
        return handler(schema=self, **kwds)


# end of file
