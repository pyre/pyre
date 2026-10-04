#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that the descriptions of the visualization factories name their slots the way the c++
factories they describe name their accessors, so a flow drawn in python means the same thing
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
            "parametric": (["signal"], ["parametric"]),
            "power": (["signal"], ["power"]),
        },
        # the selectors
        pyre.viz.selectors: {
            "amplitude": (["signal"], ["amplitude"]),
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
        },
        # the codecs
        pyre.viz.codecs: {
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
    assert pyre.viz.filters.parametric().interval == (0, 1)
    assert pyre.viz.colormaps.hl().threshold == 0.4

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
