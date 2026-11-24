# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
The description of tables and their columns
"""

# the special values {NULL} and {DEFAULT}
from .literals import null, default

# the slots for the values of prepared statements
from .Parameter import Parameter as parameter

# cascade action markers for foreign keys
from .actions import noAction, restrict, cascade, setNull, setDefault

# the base of the column types
from .Measure import Measure as measure

# references to the keys of other tables
from .Reference import Reference as reference

# tables
from .Table import Table as table

# end of file
