# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


class Field:
    """
    The base class for record descriptors. See {pyre.records.Record} for details.
    """

    # types
    from ..schema.Object import Object


    # public data
    name = None # my name
    default = None # my default value
    optional = False # am i allowed to be uninitialized?
    type = Object # my type; most likely one of the pyre.schema type declarators
    validators = () # the chain of functions that inspect and validate my value
    converters = () # the chain of transformation necessary to produce a value in my native type


# end of file 
