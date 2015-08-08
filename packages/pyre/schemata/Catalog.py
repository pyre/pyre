# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#


# superclass
from .Mapping import Mapping


# declaration
class Catalog(Mapping):
    """
    The catalog type declarator
    """


    # constants
    typename = 'catalog' # the name of my type
    container = dict # the container i represent


# end of file
