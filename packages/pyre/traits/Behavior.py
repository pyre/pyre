# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


# superclass
from .Trait import Trait


# declaration
class Behavior(Trait):
    """
    The base class for component methods that are part of its external interface
    """

    
    # public data
    method = None # the actual callable in the component declaration


    # meta-methods
    def __init__(self, method, **kwds):
        super().__init__(**kwds)
        self.__doc__ = method.__doc__
        self.method = method
        return


    def __get__(self, instance, cls=None):
        """
        Access to the behavior: dispatch to the encapsulated method
        """
        # bind my method and return the resulting callable
        return self.method.__get__(instance, cls)


    def __set__(self, instance, value):
        """
        Disable writing to behavior descriptors
        """
        raise TypeError(
            "can't modify {.name!r}, part of the public interface of {.pyre_name!r}"
            .format(self, instance))


# end of file 
