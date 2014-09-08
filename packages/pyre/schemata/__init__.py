# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#


# the trivial type
from .Schema import Schema as identity
# simple types
from .Boolean import Boolean as bool
from .Decimal import Decimal as decimal
from .Float import Float as float
from .Fraction import Fraction as fraction
from .INet import INet as inet
from .Integer import Integer as int
from .String import String as str

# more complex types
from .Date import Date as date
from .Dimensional import Dimensional as dimensional
from .Time import Time as time
from .URI import URI as uri

# containers
from .Sequence import Sequence as sequence
from .Array import Array as array
from .List import List as list
from .Set import Set as set
from .Tuple import Tuple as tuple

from .Mapping import Mapping as mapping
from .Catalog import Catalog as catalog

# meta-types
from .Component import Component as component
from .InputStream import InputStream as istream
from .OutputStream import OutputStream as ostream


# put the schemata in piles
basic = (identity, bool, decimal, float, fraction, inet, int, str)
composite = (date, dimensional, time, uri)
containers = (sequence, array, list, set, tuple, mapping, catalog)
meta = (istream, ostream)
# all of them
schemata = basic + composite + containers + meta

# type categories
sequences = { list, set, tuple }
mappings = { catalog }
numeric = { bool, decimal, dimensional, float, int }


# grant access to the type decorator
from .Typed import Typed as typed


# end of file 
