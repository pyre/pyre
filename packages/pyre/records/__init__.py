# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


# data records
from .Record import Record as record
from .DynamicRecord import DynamicRecord as dynamicrecord

from ..descriptors.Descriptor import Descriptor as entry
field = entry.variable
derivation = entry.operator


# persistence
from .CSV import CSV as csv


# access to the type specifiers
from .. import schemata
# access to the typed field declarators
from ..descriptors import bool, dimensional, decimal, float, inet, int, str, uri


# end of file 
