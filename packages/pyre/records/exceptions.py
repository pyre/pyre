# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


"""
Definitions for all the exceptions raised by this package
"""


from ..framework.exceptions import FrameworkError


class RecordError(FrameworkError):
    """
    The base class of all exceptions raised by this package
    """


class SourceSpecificationError(RecordError):
    """
    A method that reads records from external input sources was given an invalid input
    specification
    """

    def __init__(self, **kwds):
        reason = "invalid input source specification"
        super().__init__(description=reason, **kwds)
        return


# end of file 
