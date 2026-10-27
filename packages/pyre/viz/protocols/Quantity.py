# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
import pyre


# the protocol for the products that hold numbers
class Quantity(pyre.flow.specification, family="pyre.viz.quantities"):
    """
    The protocol for products that hold numbers: tiles, which hold one in each cell of a grid,
    and scalars, which hold just one; the slots that take either one expect a quantity
    """

    # the c++ product templates whose instantiations satisfy me; a quantity is any of the ones
    # its refinements name, so it names none of its own
    pyre_products = ()


# end of file
