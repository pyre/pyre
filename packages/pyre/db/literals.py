# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


# the node factory
from .Lazy import Lazy


# the constants
null = Lazy.literal(value='NULL')
default = Lazy.literal(value='DEFAULT')


# end of file
