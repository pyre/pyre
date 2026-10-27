#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check the operators: the unary and binary protocols are building blocks with no family of their own,
the components live under the family of the operators, and a short name resolves through the
operator protocol
"""


def test():
    # support
    import pyre

    # the protocols
    protocols = pyre.viz.protocols
    # the operators
    operators = pyre.viz.operators
    # the building blocks, which components import directly
    from pyre.viz.protocols.Unary import Unary
    from pyre.viz.protocols.Binary import Binary

    # the unary operators refine the operator protocol
    assert issubclass(Unary, protocols.operator)
    # and so do the binary ones
    assert issubclass(Binary, protocols.operator)
    # but have no family, so they take no part in resolving names
    for block in (Unary, Binary):
        # no family
        assert block.pyre_family() is None
        # and not among the public ancestors of anything
        assert block not in list(block.pyre_public())

    # the amplitude
    amplitude = operators.amplitude()
    # lives under the operators
    assert amplitude.pyre_family() == "pyre.viz.operators.amplitude"
    # is a unary operator
    assert issubclass(amplitude.pyre_implements, Unary)
    # and not a binary one
    assert not issubclass(amplitude.pyre_implements, Binary)
    # reads complex samples
    assert amplitude.pyre_trait(alias="signal").protocol is pyre.viz.tiles.complex
    # and writes magnitudes
    assert amplitude.pyre_trait(alias="amplitude").protocol is pyre.viz.tiles.magnitude
    # and is not an accessor
    assert not hasattr(pyre.viz.accessors, "amplitude")

    # the phase
    phase = operators.phase()
    # lives under the operators, next to the amplitude
    assert phase.pyre_family() == "pyre.viz.operators.phase"
    # is a unary operator
    assert issubclass(phase.pyre_implements, Unary)
    # and not a binary one
    assert not issubclass(phase.pyre_implements, Binary)
    # reads complex samples
    assert phase.pyre_trait(alias="signal").protocol is pyre.viz.tiles.complex
    # and writes reals
    assert phase.pyre_trait(alias="phase").protocol is pyre.viz.tiles.real
    # and is not an accessor
    assert not hasattr(pyre.viz.accessors, "phase")

    # the sum
    add = operators.add()
    # lives under the operators too
    assert add.pyre_family() == "pyre.viz.operators.add"
    # and is a binary operator
    assert issubclass(add.pyre_implements, Binary)
    # and not a unary one
    assert not issubclass(add.pyre_implements, Unary)

    # the rest of the arithmetic
    for name in ("subtract", "multiply", "divide"):
        # each one
        operator = getattr(operators, name)()
        # lives under the operators
        assert operator.pyre_family() == f"pyre.viz.operators.{name}"
        # is a binary operator
        assert issubclass(operator.pyre_implements, Binary), name
        # whose operands and result are quantities, tiles or scalars
        for slot in ("op1", "op2", "result"):
            # one slot at a time
            assert operator.pyre_trait(alias=slot).protocol is pyre.viz.quantity, (name, slot)

    # the palette asks the operator protocol for its implementers
    found = {
        implementer.pyre_family()
        for _, _, implementer in protocols.operator.pyre_locateAllImplementers(namespace="pyre")
    }
    # and finds both kinds: the amplitude
    assert "pyre.viz.operators.amplitude" in found
    # the phase
    assert "pyre.viz.operators.phase" in found
    # and the sum
    assert "pyre.viz.operators.add" in found

    # a component with a slot for an operator
    class Pipeline(pyre.component, family="tests.pyre.viz.pipeline"):
        """
        Hold an operator
        """

        # the operator
        operator = protocols.operator()

    # make one
    pipeline = Pipeline(name="pipeline")
    # name the operator by its short name, as a configuration file would
    pipeline.operator = "amplitude"
    # which resolves to an instance of the amplitude
    assert isinstance(pipeline.operator, amplitude)

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
