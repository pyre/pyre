# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#

from ..calc.Node import Node
from ..calc.Expression import Expression


class Variable(Node):
    """
    The object used to hold the values of all configurable items

    All evaluator nodes are expressions. Their values are gathered from configuration files and
    the command line as strings and they are later converted into their target type by the
    binding process. They are stored as expressions to enable arithmentic, access to builtin
    functions and references to other variables
    """


# end of file 
