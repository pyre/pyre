#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Making the products of a factory whose inputs hold nothing fails, naming the inputs
"""


def test() -> None:
    """
    Make the products of factories with one and with several inputs that hold nothing
    """
    # support
    import pyre

    # a specification
    class Spec(pyre.flow.specification, family="tests.pyre.flow.unbound.specs"):
        """
        The products of this test
        """

    # a factory that reads one product
    class One(pyre.flow.factory, family="tests.pyre.flow.unbound.one"):
        """
        A factory with a single input
        """

        # the input
        source = Spec.input()

    # and one that reads three
    class Three(pyre.flow.factory, family="tests.pyre.flow.unbound.three"):
        """
        A factory with three inputs
        """

        # the inputs
        red = Spec.input()  # red
        green = Spec.input()  # green
        blue = Spec.input()  # blue

    # for each factory, the inputs the failure should name
    for factory, unbound in [(One(), "'source'"), (Three(), "'red', 'green' and 'blue'")]:
        # making its products
        try:
            # by asking the factory to make them
            factory.pyre_make()
        # fails
        except factory.IncompleteFlowError as error:
            # naming the factory and its inputs
            assert error.unbound == unbound, error.unbound
            # and saying so in its description
            assert error.description.format(error) == f"{factory} has no product in {unbound}"
        # and must not succeed
        else:
            # so complain if it does
            assert False, f"{factory} made its products with nothing to read"

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
