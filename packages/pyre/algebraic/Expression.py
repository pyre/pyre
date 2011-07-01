# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


from .Node import Node


class Expression(Node):
    """
    Base class for all nodes that capture operations

    This class is really just a marker in the class hierarchy that enables clients to
    distinguish between literal nodes and nodes that capture operations.
    """


    # interface
    def pyre_patch(self, replacements):
        """
        Look through the dictionary {replacements} for any of my operands and replace them with
        the indicated nodes.
        """
        raise NotImplementedError(
            "class {.__class__.__name__!r} must implement 'pyre_patch'".format(self))


# end of file 
