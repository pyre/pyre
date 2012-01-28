# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


class ParsingError(Exception):
    """
    Error raised when there is a problem with the contents of a configuration file
    """


    # public data
    locator = None # tracking the error location
    description = None # a brief explanation about what went wrong


    def __init__(self, description, locator, **kwds):
        super().__init__(**kwds)

        self.locator = locator
        self.description = description

        return


# end of file 
