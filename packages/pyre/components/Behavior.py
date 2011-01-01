# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


from .Trait import Trait


class Behavior(Trait):
    """
    The base class for component methods that are part of its external interface
    """

    
    # public data; inherited from Trait but repeated here for clarity
    name = None # my canonical name; set at construction time or binding name
    aliases = None # the set of alternative names by which I am accessible
    tip = None # a short description of my purpose and constraints
    # additional state
    method = None # the actual callable in the component declaration
    # predicate that indicates whether this trait is subject to runtime configuration
    pyre_isConfigurable = False


    # meta methods
    def __init__(self, method, **kwds):
        super().__init__(**kwds)
        self.method = method
        self.__doc__ = method.__doc__
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
