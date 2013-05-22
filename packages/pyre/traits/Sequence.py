# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


# externals
from .. import schemata
# superclass
from .Property import Property


class Sequence(Property):
    """
    The base class for attribute descriptors that are containers
    """


    # the default schema for my contents; must be another trait descriptor, not a bare
    # converter from {pyre.schemata}
    from .Object import Object as identity


    # framework support
    def macro(self, model):
        """
        Return my preferred macro processor
        """
        # ask the content type descriptor
        return self.schema.schema.macro(model=model)


    # meta-methods
    def __init__(self, default, schema=identity, **kwds):
        # chain up
        super().__init__(default=default, **kwds)
        # set my schema as a sequence of whatever type the schema of my contents is
        self.schema = schemata.sequence(schema=schema)
        # all done
        return


# end of file 
