# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#


# superclass
from .Sequence import Sequence


# declaration
class Set(Sequence):
    """
    The set type declarator
    """


    # constants
    typename = 'set' # the name of my type
    container = set # the container I represent


# end of file 
