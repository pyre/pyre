# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


# packages
import re
import itertools
import pyre.patterns
# super-class
from ..algebraic.Hierarchical import Hierarchical as Model


# declaration
class HierarchicalModel(Model):
    """
    Storage and naming services for calc nodes

    This class assumes that the node names form a hierarchy, very much like path names. They
    are expected to be given as tuples of strings that specify the names of the "folders" at
    each level.

    HierarchicalModel provides support for links, entries that are alternate names for other
    folders.
    """


    # types
    # my node type
    from .Node import Node as node


# end of file 
