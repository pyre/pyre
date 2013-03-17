# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


# data records
from .Record import Record as record
from .DynamicRecord import DynamicRecord as dynamicrecord

from .Entry import Entry as entry
field = entry.variable
derivation = entry.operator


# persistence
from .CSV import CSV as csv


# access to the type specifiers
from .. import schemata
# access to the typed field declarators
from .fields import float, int, str


# end of file 
