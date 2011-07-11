# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


# access to the type descriptors
from .. import schema
# the base class for column descriptors
from .Column import Column
# other necessary packages
import decimal


# booleans
class Boolean(Column):
    """
    Representation for booleans
    """

    type = schema.bool

    def decl(self):
        """SQL compliant rendering of my type name"""
        return "BOOLEAN"

    def decldefault(self):
        if self.default is not None:
            return " DEFAULT {}".format('true' if self.default else 'false')
        return ""

    
# dates
class Date(Column):
    """
    Representation for dates
    """

    type = schema.date

    def decl(self):
        """SQL compliant rendering of my type name"""
        return "DATE"


# fixed precision arithmetic
class Decimal(Column):
    """
    Representation of fixed precision numbers
    """

    type = schema.decimal

    def decl(self):
        """SQL compliant rendering of my type name"""
        return "DECIMAL({}, {})".format(self.precision, self.scale)

    def __init__(self, precision, scale, default=0, **kwds):
        super().__init__(default=decimal.Decimal(default), **kwds)
        self.precision = precision
        self.scale = scale
        return


# floating point numbers
class Float(Column):
    """
    Representation of floating point numbers
    """

    type = schema.float

    def decl(self):
        """SQL compliant rendering of my type name"""
        return "DOUBLE PRECISION"

    def __init__(self, default=0.0, **kwds):
        super().__init__(default=default, **kwds)
        return


# integers
class Integer(Column):
    """
    Representation for integers
    """

    type = schema.int

    def decl(self):
        """SQL compliant rendering of my type name"""
        return "INTEGER"

    def __init__(self, default=0, **kwds):
        super().__init__(default=default, **kwds)
        return


# arbitrary length strings
class String(Column):
    """
    Representation for arbitrary length string
    """

    type = schema.int

    def decl(self):
        """SQL compliant rendering of my type name"""
        if self.maxlen == None:
            return "TEXT"
        return "VARCHAR({})".format(self.maxlen)

    def decldefault(self):
        """
        Invoked by the SQL mill to create the default value part of the declaration
        """
        if self.default is not None:
            return " DEFAULT '{}'".format(self.default)
        return ""

    def __init__(self, maxlen=None, default='', **kwds):
        super().__init__(default=default, **kwds)
        self.maxlen = maxlen
        return


# timestamps
class Time(Column):
    """
    Representation for time stamps
    """

    type = schema.time

    def decl(self):
        """SQL compliant rendering of my type name"""
        return "TIMESTAMP WITH{} TIME ZONE".format('' if self.timezone else 'OUT')

    def __init__(self, timezone=False, **kwds):
        super().__init__(**kwds)
        self.timezone = timezone
        return


# end of file 
