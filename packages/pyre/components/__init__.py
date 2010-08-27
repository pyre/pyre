# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


"""
This package contains the implementation details of the two fundamental building blocks of
application behavior in pyre: components and interfaces.

"""


# method decorators
def export(func):
    """
    Function decorator that marks a component method as part of its external interface
    """
    from .Behavior import Behavior
    return Behavior(func)


def provides(func):
    """
    Function decorator that marks an interface method as part of its required interface
    """
    from .Behavior import Behavior
    return Behavior(func)


# the component registrar factory
def newRegistar(**kwds):
    from .Registrar import Registrar
    return Registrar(**kwds)


# access to the component and interface classes
from .Component import Component as component
from .Facility import Facility as facility
from .Interface import Interface as interface
from .Property import Property as property


# end of file 
