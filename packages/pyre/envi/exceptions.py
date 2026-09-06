# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Definitions for all the exceptions raised by this package
"""

# superclass
from ..framework.exceptions import FrameworkError


# the local base
class ENVIError(FrameworkError):
    """
    The base class of all exceptions raised by the envi package
    """

    # public data
    description = "generic ENVI error"


class MissingMarkerError(ENVIError):
    """
    Exception raised when a header does not start with the ENVI marker
    """

    # public data
    description = "'{0.uri}' does not start with the ENVI marker"

    # metamethods
    def __init__(self, uri, **kwds):
        # chain up
        super().__init__(**kwds)
        # save the location
        self.uri = uri
        # all done
        return


class MalformedHeaderError(ENVIError):
    """
    Exception raised when a header line cannot be understood
    """

    # public data
    description = "'{0.uri}', line {0.line}: {0.reason}: '{0.text}'"

    # metamethods
    def __init__(self, uri, line, text, reason, **kwds):
        # chain up
        super().__init__(**kwds)
        # save the location
        self.uri = uri
        self.line = line
        # the offending text
        self.text = text
        # and what is wrong with it
        self.reason = reason
        # all done
        return


class MalformedValueError(ENVIError):
    """
    Exception raised when the value of a known keyword cannot be converted to its documented type
    """

    # public data
    description = "could not convert the value of '{0.keyword}': {0.value}"

    # metamethods
    def __init__(self, keyword, value, **kwds):
        # chain up
        super().__init__(**kwds)
        # save the keyword
        self.keyword = keyword
        # and the offending value
        self.value = value
        # all done
        return


class UnknownDataTypeError(ENVIError):
    """
    Exception raised when a header declares a data type code that ENVI does not define
    """

    # public data
    description = "unknown ENVI data type code {0.code}"

    # metamethods
    def __init__(self, code, **kwds):
        # chain up
        super().__init__(**kwds)
        # save the code
        self.code = code
        # all done
        return


# end of file
