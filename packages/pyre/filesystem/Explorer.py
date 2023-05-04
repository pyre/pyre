# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


class Explorer:
    """
    Base class for visitors of the filesystem object model
    """

    # interface
    def explore(self, node, **kwds):
        """
        Traverse the tree rooted at {node}
        """
        raise NotImplementedError(
            f"class '{type(self).__name__}' must implement 'explore'"
        )


# end of file
