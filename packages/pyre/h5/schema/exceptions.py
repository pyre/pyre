# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


"""
Definitions for all the exceptions raised by this package
"""


# superclass
from ..exceptions import H5Error


# the local base of api errors
class SchemaError(H5Error):
    """
    The base class of all exceptions raised by the {h5.schema} package
    """


# datatypes
class PathNotFoundError(SchemaError):
    """
    Exception raised when looking for a nonexistent path in a group
    """

    # the message template
    description = "path '{0.path}' not found"

    # metamethods
    def __init__(self, group, path, child, fragment, **kwds):
        # chain up
        super().__init__(**kwds)
        # save the error information
        self.group = group
        self.path = path
        self.child = child
        self.fragment = fragment
        # all done
        return

    # framework hooks
    def _pyre_report(self):
        # chain up
        yield from super()._pyre_report()
        # add more detail
        yield f"in {self.group}"
        yield f"could not find '{self.fragment}'"
        yield f"within {self.child}"
        # all done
        return


# end of file
