# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# a recipe realized for one tile shape
class Graph:
    """
    The c++ nodes a staged recipe was realized into, by the names of the nodes of the recipe;
    the graph takes itself apart when it is dismantled, or when it is used as a context manager
    and the block is over
    """

    # interface
    def dismantle(self) -> None:
        """
        Undo every binding, so the nodes can be released
        """
        # go through the bindings of the recipe
        for binding in self.recipe.bindings:
            # find the factory
            factory = self.nodes.get(binding.factory)
            # one that was made
            if factory is not None:
                # loses its binding, if it had one
                factory.unbind(slot=binding.slot)
        # let go of the nodes
        self.nodes.clear()
        # all done
        return

    # metamethods
    def __init__(self, *, recipe, nodes: dict, **kwds):
        # chain up
        super().__init__(**kwds)
        # save the recipe
        self.recipe = recipe
        # and the nodes, by name
        self.nodes = nodes
        # all done
        return

    def __getitem__(self, name: str):
        # look up the node {name}
        return self.nodes[name]

    def __enter__(self):
        # the graph is the context
        return self

    def __exit__(self, *_) -> bool:
        # take me apart
        self.dismantle()
        # and let whatever happened in the block go on its way
        return False


# end of file
