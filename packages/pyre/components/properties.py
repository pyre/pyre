# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


"""
This package provides factories for typed properties
"""

from .Facility import Facility
from .Property import Property
from .. import schema


def array(default=None):
    """
    Build an array property descriptor
    """
    descriptor = Property()
    descriptor.type = schema.array
    descriptor.default = default if default is not None else ()
    return descriptor


def bool(default=True):
    """
    Build a bool property descriptor
    """
    descriptor = Property()
    descriptor.type = schema.bool
    descriptor.default = default
    return descriptor


def dimensional(default=0):
    """
    Build a bool property descriptor
    """
    descriptor = Property()
    descriptor.type = schema.dimensional
    descriptor.default = default
    return descriptor


def facility(interface, default=None):
    """
    Build a facility descriptor
    """
    descriptor = Facility(interface=interface)
    descriptor.default = default
    return descriptor


def float(default=0):
    """
    Build a bool property descriptor
    """
    descriptor = Property()
    descriptor.type = schema.float
    descriptor.default = default
    return descriptor


def int(default=0):
    """
    Build an integer property descriptor
    """
    descriptor = Property()
    descriptor.type = schema.int
    descriptor.default = default
    return descriptor


def object(default=None):
    """
    Build a generic property descriptor
    """
    descriptor = Property()
    descriptor.type = schema.object
    descriptor.default = default
    return descriptor


def str(default=""):
    """
    Build a str property descriptor
    """
    descriptor = Property()
    descriptor.type = schema.str
    descriptor.default = default
    return descriptor


# end of file 
