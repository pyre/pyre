# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


from .Requirement import Requirement


class Role(Requirement):
    """
    The interface metaclass
    """


    def __init__(self, name, bases, attributes, **kwds):
        """
        Initialize a new class record

        Build the trait category index using the filtered attributes and register this
        interface with the registrar
        """
        return


# end of file 
