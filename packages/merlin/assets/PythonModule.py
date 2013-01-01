# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


from .Asset import Asset


class PythonModule(Asset):
    """
    Encapsulation of an asset that represents a python source file
    """


    # constants
    category = "python module"


    # implementation details
    __slots__ = ()


# end of file 
