# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2024 all rights reserved


# framework
import merlin


# base class for merlin products
class Product(
    merlin.flow.product, implements=merlin.protocols.flow.specification, internal=True
):
    """
    The base class for {merlin} products
    """


# end of file
