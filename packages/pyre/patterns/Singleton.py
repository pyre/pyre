# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# superclass
from .Type import Type


# declaration
class Singleton(Type):
    """
    Provide support for classes that create and manage a single instance

    Adapted from Michele Simionato's implementation

    N.B.: the singleton constructor is called only the first time the singleton is accessed, so
    you have to make sure that the first access is the correct one if the class has a
    non-trivial constructor. Subsequent calls do not have to worry about the constructor
    signature since it will not be invoked ever again
    """


    # constants
    null = object() # a marker to indicate an uninitialized singleton


    # metamethods
    def __init__(self, name, bases, attributes, **kwds):
        """
        Initialize a new class record
        """
        # chain up
        super().__init__(name, bases, attributes, **kwds)
        # reset the unique instance
        self.pyre_singletonInstance = self.null
        # all done
        return


    def __call__(self, **kwds):
        """
        Return the singleton instance every time the constructor is called
        """
        # get the singleton instance
        it = self.pyre_singletonInstance
        # if {it} doesn't exist yet
        if it is self.null:
            # build it
            it = super().__call__(**kwds)
            # and attach it
            self.pyre_singletonInstance = it
        # in either case, publish it
        return it


# end of file
