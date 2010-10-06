# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


from .Property import Property


class Facility(Property):
    """
    The base class for traits that must conform to a given interface
    """

    # public data; look in Property for inherited attributes
    type = None # my type; must be an Interface class record (an instance of Role)
    optional = False # facilities must be given values


    # binding interface
    def pyre_bindClass(self, configurable):
        """
        Bind this trait to the {configurable} class record
        """
        raise NotImplementedError("NYI!")


    def pyre_bindInstance(self, configurable):
        """
        Bind this trait to the {configurable} instance
        """
        raise NotImplementedError("NYI!")


    # meta methods
    def __init__(self, interface, default=None, **kwds):
        super().__init__(**kwds)
        self.type = interface
        self.default = default
        return


    # exceptions
    from .exceptions import FacilitySpecificationError


# end of file 
