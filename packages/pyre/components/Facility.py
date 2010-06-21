# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


from .Property import Property
from .Component import Component


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
        print("{0.name!r}: type={0.type!r}".format(self))
        return self.type.pyre_cast(name=self.name, value=value)

    

# end of file 
