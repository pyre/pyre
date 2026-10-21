# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# externals
import io
import sys

# superclasses
from .Schema import Schema
from ..framework.Dashboard import Dashboard


# declaration
class OutputStream(Schema, Dashboard):
    """
    A representation of output streams
    """

    # constants
    mode = "w"
    typename = "ostream"
    complaint = "could not use {0.value!r} as an output stream"

    # types
    from . import uri

    # interface
    def coerce(self, value, **kwds):
        """
        Attempt to convert {value} into an open output stream
        """
        # text
        if isinstance(value, str):
            # the value is the special string "stdout"
            if value == "stdout" or value == "<stdout>":
                # return the process stdout
                return sys.stdout
            # the value is the special string "stderr"
            if value == "stderr" or value == "<stderr>":
                # return the process stderr
                return sys.stderr
            # anything else, the framework fileserver knows how to open
            return self.pyre_fileserver.open(uri=value, mode=self.mode)
        # if the {value} is a uri
        if isinstance(value, self.uri.locator):
            # assume that the framework fileserver knows how to deal with it
            return self.pyre_fileserver.open(uri=value, mode=self.mode)
        # streams that are already open
        if isinstance(value, io.IOBase):
            # are left alone
            return value
        # all other types are incompatible, for now
        raise self.CastingError(value=value, description=self.complaint)

    def string(self, value):
        """
        Render value as a string that can be persisted for later coercion
        """
        # respect {None}
        if value is None:
            #  by leaving it alone
            return None
        # my value knows
        return value.name

    def json(self, value):
        """
        Generate a JSON representation of {value}
        """
        # represent as a string
        return self.string(value)

    # visiting
    def _pyre_identify(self, authority, **kwds):
        """
        Let {authority} know i am an output stream
        """
        # attempt to
        try:
            # ask {authority} for my handler
            handler = authority._pyre_onOutputStream
        # if it doesn't understand
        except AttributeError:
            # chain up
            return super()._pyre_identify(authority=authority, **kwds)
        # otherwise, invoke the handler
        return handler(schema=self, **kwds)

    # meta-methods
    def __init__(self, default="stdout", mode=mode, **kwds):
        # chain up
        super().__init__(default=default, **kwds)
        # save my mode
        self.mode = mode
        # all done
        return


# end of file
