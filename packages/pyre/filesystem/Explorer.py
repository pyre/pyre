# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


class Explorer:
    """
    Base class for visitors of the filesystem object model
    """


    # constants
    from . import separator


    # interface
    def explore(self, node, **kwds):
        """
        Traverse the tree rooted at {node}
        """
        raise NotImplementedError(
            "class {.__name__!r} must implement 'explore'".format(type(self)))


# end of file 
