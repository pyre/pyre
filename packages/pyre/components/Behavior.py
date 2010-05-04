# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


from .Trait import Trait


class Behavior(Trait):
    """
    """


    # public data
    name = None # my canonical name; set at construction time or binding name
    tip = None # a short description of my purpose and constraints; see doc below


    # meta methods
    def __init__(self, method, **kwds):
        super().__init__(**kwds)
        self._method = method
        self.__doc__ = method.__doc__
        return


    def __get__(self, instance, cls=None):
        """
        Dispatch to the encapsulated method
        """
        # if the caller specified the instance, bind _method to the instance and return it
        if instance:
            return self._method.__get__(instance, cls)
        # otherwise, interpret this as a request for the descriptor
        return self


    # framework data
    _pyre_category = "behaviors"


# end of file 
