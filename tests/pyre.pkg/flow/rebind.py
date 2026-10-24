#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Handing a slot of a factory the product it holds already changes nothing, so a product that was
made stays made, whether or not the factory has a name; a different product, or a change to a
setting, still invalidates what the factory makes
"""


def test() -> None:
    """
    Hand the slots of a named and an anonymous factory their own products
    """
    # support
    import pyre

    # a specification
    class Spec(pyre.flow.specification, family="tests.pyre.flow.rebind.specs"):
        """
        The products of this test
        """

        # the default implementation
        @classmethod
        def pyre_default(cls, **kwds):
            """
            The products of this test are held in memory
            """
            # hand it off
            return Product

    # a product
    class Product(pyre.flow.product, family="tests.pyre.flow.rebind.product", implements=Spec):
        """
        A product that holds nothing
        """

    # a factory that reads one product and writes another
    class Factory(pyre.flow.factory, family="tests.pyre.flow.rebind.factory"):
        """
        A factory with a setting, an input, and an output
        """

        # a setting
        scale = pyre.properties.float()
        scale.default = 1.0
        # the input
        source = Spec.input()
        # and the output
        target = Spec.output()

    # for a named factory and an anonymous one
    for factory in (Factory(name="tests.pyre.flow.rebind.named"), Factory()):
        # its output
        made = factory.target
        # made
        made.pyre_done()
        # and an input
        source = Product()
        # made too
        source.pyre_done()
        # bound to the factory
        factory.source = source
        # and the output made again after the binding
        factory.target.pyre_done()

        # handing the output the product it holds
        factory.target = made
        # leaves it made
        assert factory.target is made and not made.pyre_stale
        # and so does handing the input the product it holds
        factory.source = source
        # leaves the output made
        assert not made.pyre_stale

        # a change to a setting
        factory.scale = 2.0
        # invalidates what the factory makes
        assert made.pyre_stale
        # until it is made again
        made.pyre_done()

        # and a different product
        other = Product()
        # in the output
        factory.target = other
        # is stale until it is made
        assert factory.target is other and other.pyre_stale

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
