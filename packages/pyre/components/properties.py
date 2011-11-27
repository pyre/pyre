# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


"""
This package provides factories for typed properties
"""

from .Facility import Facility
from .Property import Property
from .OutputFile import OutputFile
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
    Build a property descriptor with units
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
    Build a float property descriptor
    """
    descriptor = Property()
    descriptor.type = schema.float
    descriptor.default = default
    return descriptor


def inet(default=schema.inet.any):
    """
    Build a internet address descriptor
    """
    descriptor = Property()
    descriptor.type = schema.inet
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


def outputfile(mode=OutputFile.mode, default=OutputFile.default):
    """
    Build a descriptor for an output file
    """
    descriptor = OutputFile()
    descriptor.type = descriptor # output files are their schema specifications
    descriptor.mode = mode
    descriptor.default = default
    return descriptor


def str(default=""):
    """
    Build a string property descriptor
    """
    descriptor = Property()
    descriptor.type = schema.str
    descriptor.default = default
    return descriptor


# end of file 
