# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#


# exceptions
from ..exceptions import NexusError


# local anchor
class ProtocolError(NexusError):
    """
    Base exceptions for all error conditions detected by http components
    """

    # meta-methods
    def __init__(self, description, **kwds):
        # chain up
        super().__init__(**kwds)
        # store
        self.description = description
        # all done
        return


# specific errors
class BadRequestSyntaxError(ProtocolError):
    """
    Bad request
    """
    # state
    code = 400
    description = "Bad request syntax or unsupported method"

    # meta-methods
    def __init__(self, description=description, **kwds):
        # chain up
        super().__init__(description=description, **kwds)
        # all done
        return


class EntityTooLargeError(ProtocolError):
    """
    Request entity too large
    """
    # state
    code = 413
    description = "Entity is too large"

    # meta-methods
    def __init__(self, description=description, **kwds):
        # chain up
        super().__init__(description=description, **kwds)
        # all done
        return


# end of file
