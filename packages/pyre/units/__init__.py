# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#

"""
This package provides support for working with diensional quantities

It contains definitions for all seven fundamental and twenty-one derived SI units, as well as support for units from other systems
"""

# factories
def unit(**kwds):
    """
    Create and return an instance of a Diminesional.

    This factory grants access to the low level interfeace, useful for building dimensional
    objects directly from their representation. However, manipulating one of the predefined
    unit objects should be sufficient for most uses. Please let me know if you find something
    that cannot be done any other way and you find yourself resorting to building dimensionals
    directly.
    """
    from .Dimensional import Dimensional
    return Dimensional(**kwds)


# end of file 
