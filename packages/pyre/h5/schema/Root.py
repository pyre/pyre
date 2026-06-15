# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
import pyre

# superclass
from .Group import Group


# the root of a product schema tree
class Root(Group):
    """
    The root of a product schema tree

    The root is the one node that sees the whole tree, so it owns the index of named
    shape dimensions that correlated dataset shapes refer to. It is also the node that
    carries the product's absolute mount point, its {_pyre_location}.
    """

    # metamethods
    def __init__(self, **kwds):
        # chain up
        super().__init__(**kwds)
        # build my index of named shape dimensions; these are reactive {pyre.calc} nodes,
        # so that setting a product dimension propagates to every dependent dataset shape.
        # it is an instance attribute: the nodes are structural, but their values bind per
        # realization, so realizations must not share one index
        self._pyre_shapes = pyre.calc.model()
        # all done
        return


# end of file
