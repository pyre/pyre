# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


from .Property import Property


class Facility(Property):
    """
    Base class for traits that are supposed to be bound to other components
    """


    # private data
    _pyre_category = "facilities"


    # interface
    def pyre_cast(self, value):
        """
        Convert {value} to an actual component
        """
        print("NYI: facility needs to cast values to components")
        return value

    

# end of file 
