# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2016 all rights reserved
#


# exceptions
from ..framework.exceptions import FrameworkError


class ParsingError(FrameworkError):
    """
    Exception raised on failed attempts to convert a string value to one of the primitive types
    """

    # meta-methods
    def __init__(self, value, **kwds):
        # chain up
        super().__init__(**kwds)
        # save the error info
        self.value = value
        # all done
        return


# end of file
