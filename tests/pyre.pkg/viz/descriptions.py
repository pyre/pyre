#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that the descriptions of the visualization factories name their slots the way the c++
factories and iterators they describe name them, so a flow drawn in python means the same thing
as the one that runs
"""


def test():
    # support
    import pyre

    # the factories, by protocol, with the names of their input and output slots
    expected = {
        # the filters
        pyre.viz.filters: {
            "affine": (["signal"], ["affine"]),
            "constant": ([], ["tile"]),
            "cycle": (["signal"], ["cycle"]),
            "decimate": (["signal"], ["decimated"]),
            "geometric": (["signal"], ["bin"]),
            "logsaw": (["signal"], ["logsaw"]),
            "polarsaw": (["signal"], ["polarsaw"]),
            "power": (["signal"], ["power"]),
            "uniform": (["signal"], ["bin"]),
        },
        # the operators
        pyre.viz.operators: {
            "add": (["op1", "op2"], ["sum"]),
            "amplitude": (["signal"], ["amplitude"]),
            "multiply": (["op1", "op2"], ["product"]),
        },
        # the selectors
        pyre.viz.selectors: {
            "imaginary": (["signal"], ["imaginary"]),
            "phase": (["signal"], ["phase"]),
            "real": (["signal"], ["real"]),
        },
        # the colormaps
        pyre.viz.colormaps: {
            "gray": (["data"], ["red", "green", "blue"]),
            "hl": (["hue", "luminosity"], ["red", "green", "blue"]),
            "hsb": (["hue", "saturation", "brightness"], ["red", "green", "blue"]),
            "hsl": (["hue", "saturation", "luminosity"], ["red", "green", "blue"]),
            "oklch": (["lightness", "chroma", "hue"], ["red", "green", "blue"]),
        },
        # the normalizers
        pyre.viz.normalizers: {
            "parametric": (["signal"], ["normalized"]),
        },
        # the encoders
        pyre.viz.encoders: {
            "bmp": (["red", "green", "blue"], ["image"]),
        },
    }
    # go through the packages
    for package, factories in expected.items():
        # and their factories
        for name, (inputs, outputs) in factories.items():
            # make one
            factory = getattr(package, name)()
            # its inputs must be named as expected, in the order they are declared
            assert [trait.name for trait in factory.pyre_inputTraits] == inputs
            # and so must its outputs
            assert [trait.name for trait in factory.pyre_outputTraits] == outputs

    # the settings that the c++ factories take, with their defaults
    assert pyre.viz.filters.decimate().level == 0
    assert pyre.viz.normalizers.parametric().interval == (0, 1)
    assert pyre.viz.colormaps.hl().threshold == 0.4
    assert pyre.viz.filters.geometric().bins == 10
    assert pyre.viz.filters.geometric().ratio == 2
    assert pyre.viz.filters.uniform().bins == 10

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
