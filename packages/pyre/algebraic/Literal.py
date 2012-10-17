# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


class Literal:
    """
    Class that encapsulates values encountered in expressions that are not instances of members
    of the {Node} class hierarchy.
    """


    # public data
    span = () # literals are not proper nodes so their span is empty
    operands = () # literals have no operands
    variables = () # empty span
    operators = () # empty span


# end of file 
