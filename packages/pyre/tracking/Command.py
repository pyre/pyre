# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


# declaration
class Command:
    """
    A locator that records the position of a command line argument 
    """


    # constant
    source = 'command line: {!r}'


    # meta methods
    def __init__(self, arg):
        self.arg = arg
        return


    def __str__(self):
        return self.source.format(self.arg)


    # implementation details
    __slots__ = 'arg',


# end of file 
