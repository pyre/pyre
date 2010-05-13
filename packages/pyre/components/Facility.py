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


    # public data
    interface = None # the interface specification that compatible components must satisfy


    # private data
    _pyre_category = "facilities"
    

# end of file 
