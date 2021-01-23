# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2021 all rights reserved


# declaration
class Command:
    """
    A locator that records the position of a command line argument
    """


    # metamethods
    def __init__(self, arg):
        # save the argument name
        self.arg = arg
        # all done
        return


    def __str__(self):
        # easy enough
        return f"from the command line argument '{self.arg}'"


    # implementation details
    __slots__ = 'arg',


# end of file
