# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


class Command:
    """
    Locator that records the position of a command line argument
    """


    # public data
    source = 'command line, arg {}'


    # meta methods
    def __init__(self, arg, **kwds):
        super().__init__(**kwds)
        self.arg = arg
        return


    def __str__(self):
        return self.source.format(self.arg)


# end of file 
