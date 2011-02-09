# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


from .Expression import Expression


class Binary(Expression):
    """
    Base class for nodes that capture binary operations
    """


    # traversal of the nodes in my expression tree
    @property
    def pyre_dependencies(self):
        """
        Traverse my expression tree looking for leaf nodes
        """
        # visit my left operand
        for node in self.op1.pyre_dependencies:
            # yield any nodes discovered
            yield node
        # and now my right operand
        for node in self.op2.pyre_dependencies:
            # yield any nodes discovered
            yield node
        # all done
        return


    # interface
    def pyre_patch(self, replacements):
        """
        Look through the dictionary {replacements} for any of my operands and replace them with
        the indicated nodes.
        """
        # check whether my left operand shows in the map
        if self.op1 in replacements:
            # it does; replace it
            self.op1 = replacements[self.op1]
        # otherwise
        else:
            # pass the replacement map down
            self.op1.pyre_patch(replacements)

        # check whether my right operand shows in the map
        if self.op2 in replacements:
            # it does; replace it
            self.op2 = replacements[self.op2]
        # otherwise
        else:
            # pass the replacement map down
            self.op2.pyre_patch(replacements)
        # all done
        return


    # meta methods
    def __init__(self, op1, op2, **kwds):
        super().__init__(**kwds)
        self.op1 = op1
        self.op2 = op2
        return
    

# end of file 
