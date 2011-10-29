# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


# superclass
from ..algebraic.Literal import Literal as Base


class Literal(Base):
    """
    Class that encapsulates values encountered in expressions that are not instance of members
    of the {Entry} class hierarchy.
    """


    # types
    from ..calc.Node import Node as node


    # interface
    def buildNode(self, stream, model):
        """
        Extract a value from {stream} and use it to build a {pyre.calc} node 
        """
        # easy enough
        return self.node.literal(value=self.value)


    def extract(self, stream, cache):
        """
        Compute my value by returning the encapsulated constant 
        """
        # easy enough...
        return self.value

        
# end of file 
