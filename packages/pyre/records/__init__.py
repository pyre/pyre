# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# externals
from .. import descriptors

# the kinds of fields
field = descriptors.stem  # the base of every field
measure = field.variable  # fields whose values are given
derivation = field.operator  # fields whose values are computed from other fields
literal = field.literal  # constants in the expressions of derivations

# the typed field declarators, for the basic types
bool = descriptors.bool  # truth values
decimal = descriptors.decimal  # fixed point numbers
float = descriptors.float  # floating point numbers
inet = descriptors.inet  # internet addresses
int = descriptors.int  # integers
identity = descriptors.identity  # values taken as they are
str = descriptors.str  # strings
# and for the more complex ones
date = descriptors.date  # dates
dimensional = descriptors.dimensional  # quantities with units
time = descriptors.time  # times of day
uri = descriptors.uri  # resource identifiers

# the decorators that attach processing steps to fields
converter = descriptors.converter  # turn a raw value into one of the field's type
normalizer = descriptors.normalizer  # bring a value to its canonical form
validator = descriptors.validator  # check that a value is acceptable

# the base class for field selectors
from .Selector import Selector as selector

# the record metaclass
from .Templater import Templater as templater

# access to the record class
from .Record import Record as record

# data extraction from formatted streams
from .CSV import CSV as csv

# end of file
