# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


class Reference:
    """
    A node that refers to another node
    """

    # interface
    def getValue(self):
        """
        Compute and return my value
        """
        # get my referent
        referent, = self.operands
        # and ask him for his value
        return referent.value
        

    # meta methods
    def __init__(self, node, **kwds):
        super().__init__(operands=(node,), **kwds)
        # all done
        return


# end of file 
