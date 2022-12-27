# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# superclass
from .Device import Device


# swallow all requests to record a message
class Trash(Device):
    """
    Journal device that ignores all requests to write a message
    """

    # constants
    name = "trash"


    # interface
    def alert(self, entry):
        """
        Generate an alert
        """
        # do nothing
        return self


    def help(self, entry):
        """
        Generate a help screen
        """
        # do nothing
        return self


    def memo(self, entry):
        """
        Generate a memo
        """
        # do nothing
        return self


    # metamethods
    def __init__(self, name=name,  **kwds):
        # chain up
        super().__init__(name=name, **kwds)
        # all done
        return


# end of file
