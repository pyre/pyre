# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#

"""
This package provides support for working with dimensional quantities

It contains definitions for all seven fundamental and twenty-one derived SI units, as well as
support for units from other systems
"""


# factories
def dimensional(**kwds):
    """
    Create and return an instance of a Dimensional.

    This factory grants access to the low level interface, useful for building dimensional
    objects directly from their representation. However, manipulating one of the predefined
    unit objects should be sufficient for most uses. Please let me know if you find something
    that cannot be done any other way and you find yourself resorting to building dimensional
    quantities directly.
    """
    from .Dimensional import Dimensional
    return Dimensional(**kwds)


def parser(**kwds):
    """
    Return the unit parser singleton

    The unit parser converts string representations of dimensional quantities into instances of
    Dimensional
    """
    from .Parser import Parser
    return Parser(**kwds)


def modules():
    """
    Build a list of all available modules
    """
    from . import (
        SI,
        angle, area, energy, force, length, mass, power, pressure,
        speed, substance, temperature, time, volume
        )

    return locals().values()


# end of file 
