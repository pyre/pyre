# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


"""
This package provides the declaration mechanisms for classdata and associated metadata

The motivation comes from the need to extend the python @property mechanism to attributes that
have special meaning in specific contexts, and may require additional information about an
attribute.

The orginal use case for this functionality came from the pyre inventory mechanisms,
i.e. support for configuring and validating the public state of components. Inventory items
require some form of type checking, resonable default values, and perhaps extra validation that
is accomplished by attaching cnstraint to the attribute descriptors and enforcing them during
assignment. Other metadata that has been found to be useful are tips, i.e. short strings that
give quick guidance on the intent and proper use of an inventory item, and docs, which contain
more extensive documentation.

A similar functionality was developed separately in pyre.db to enable the description of
classes that correspond to database tables, and whose instances were records in these
tables. There the descriptor mechanism provided a convenient way to attach the datatype of the
table columns so that the correct SQL declaration could be generated automatically.

These implementations have a lot in common, so pyre.schema is an attempt to abstract the common
themes into an ancestor package and simplify the two implementations through refactoring.

The XML primitive built-in datatypes
string
boolean
decimal
float
double
duration
dateTime
time
date
gYearMonth
gYear
gMonthDay
gDay
gMonth
hexBinary
base64Binary
anyURI
QName
NOTATION
"""


# simple types

from .Float import Float as float
from .Integer import Integer as int
from .Object import Object as object


# end of file 
