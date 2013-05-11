# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


# access to the type descriptors
from .. import schemata
# the base class for field descriptors
from .Field import Field
# other necessary packages
import decimal


# booleans
class Boolean(Field):
    """
    Representation for booleans
    """

    schema = schemata.bool

    def rep(self, value):
        """SQL compliant rendering of my value"""
        return 'true' if value else 'false'

    def decl(self):
        """SQL compliant rendering of my type name"""
        return "BOOLEAN"

    def decldefault(self):
        """SQL compliant rendering of my default value"""
        if self.default is not None:
            return " DEFAULT {}".format(self.rep(self.default))
        return ""

    
# dates
class Date(Field):
    """
    Representation for dates
    """

    schema = schemata.date

    def rep(self, value):
        """SQL compliant rendering of my value"""
        raise NotImplementedError("NYI!")

    def decl(self):
        """SQL compliant rendering of my type name"""
        return "DATE"


# fixed precision arithmetic
class Decimal(Field):
    """
    Representation of fixed precision numbers
    """

    schema = schemata.decimal

    def rep(self, value):
        """SQL compliant rendering of my value"""
        return str(value)

    def decl(self):
        """SQL compliant rendering of my type name"""
        return "DECIMAL({}, {})".format(self.precision, self.scale)

    def __init__(self, precision, scale, default=0, **kwds):
        super().__init__(default=decimal.Decimal(default), **kwds)
        self.precision = precision
        self.scale = scale
        return


# floating point numbers
class Float(Field):
    """
    Representation of floating point numbers
    """

    schema = schemata.float

    def rep(self, value):
        """SQL compliant rendering of my value"""
        return str(value)

    def decl(self):
        """SQL compliant rendering of my type name"""
        return "DOUBLE PRECISION"

    def __init__(self, default=0.0, **kwds):
        super().__init__(default=default, **kwds)
        return


# integers
class Integer(Field):
    """
    Representation for integers
    """

    schema = schemata.int

    def rep(self, value):
        """SQL compliant rendering of my value"""
        return str(value)

    def decl(self):
        """SQL compliant rendering of my type name"""
        return "INTEGER"

    def __init__(self, default=0, **kwds):
        super().__init__(default=default, **kwds)
        return


# foreign keys
class Reference(Field):
    """
    Representation of foreign keys
    """

    def onDelete(self, action):
        """
        Set the action to perform when the target record is deleted. See {pyre.db.actions} for
        details
        """
        # mark
        self._foreign.delete = action
        # and return
        return

    def onUpdate(self, action):
        """
        Set the action to perform when the target record is updated. See {pyre.db.actions} for
        details
        """
        # mark
        self._foreign.update = action
        # and return
        return

    def rep(self, value):
        """SQL compliant rendering of my value"""
        # delegate to the field to which i refer
        return self.referent.rep(value)

    def decl(self):
        """SQL compliant  rendering of my type name"""
        # delegate to my referent
        return self.referent.decl()

    def __init__(self, **kwds):
        super().__init__()

        # set up my foreign key
        self._foreign = self.ForeignKey(**kwds)

        # get the field reference recorded by the foreign key
        ref = self._foreign.reference
        # if the reference mentions a field explicitly
        if ref.field is not None:
            # save it
            field = ref.field
        # otherwise
        else:
            raise NotImplementedError("NYI!")

        # store my referent
        self.referent = field
        # and my type
        self.schema = field.schema

        # all done
        return


# arbitrary length strings
class String(Field):
    """
    Representation for arbitrary length strings
    """

    schema = schemata.str

    def rep(self, value):
        """SQL compliant rendering of my value"""
        return "'{}'".format(value.replace("'", "''"))

    def decl(self):
        """SQL compliant rendering of my type name"""
        if self.maxlen == None:
            return "TEXT"
        return "VARCHAR({})".format(self.maxlen)

    def decldefault(self):
        """SQL compliant rendering of my default value"""
        if self.default is not None:
            return " DEFAULT {}".format(self.rep(self.default))
        return ""

    def __init__(self, maxlen=None, default='', **kwds):
        super().__init__(default=default, **kwds)
        self.maxlen = maxlen
        return


# timestamps
class Time(Field):
    """
    Representation for time stamps
    """

    schema = schemata.time

    def rep(self, value):
        """SQL compliant rendering of my value"""
        raise NotImplementedError("NYI!")

    def decl(self):
        """SQL compliant rendering of my type name"""
        return "TIMESTAMP WITH{} TIME ZONE".format('' if self.timezone else 'OUT')

    def __init__(self, timezone=False, **kwds):
        super().__init__(**kwds)
        self.timezone = timezone
        return


# end of file 
