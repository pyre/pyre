# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
import typing


# the edges of a recipe
class Binding(typing.NamedTuple):
    """
    A slot of a factory, and the product bound to it, all by name
    """

    # the name of the factory
    factory: str
    # the name of its slot
    slot: str
    # and the name of the product
    product: str


# end of file
