# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


# superclass
from .Templater import Templater


# declaration
class Mutable(Templater):
    """
    Metaclass for records whose entries are mutable.

    Mutable records are implemented using tuples of {pyre.calc} nodes. As a result, the values
    of fields may be modified after the original data ingestion, and all derivations are
    updated dynamically.
    """


# end of file 
