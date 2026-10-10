#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that the tile specifications refine one another by inheritance, by what their cells hold,
and that a slot typed by a refinement takes a tile of any storage strategy, since what a tile
holds is a declaration of the slot, not a property of the storage; and that the components of
the amplitude pipeline type their slots by them, from complex samples to an image
"""


def test():
    # support
    import pyre

    # the specifications
    tiles = pyre.viz.tiles
    # every one of them refines the tile specification
    for spec in (tiles.complex, tiles.real, tiles.magnitude, tiles.unit, tiles.channel):
        # by inheritance
        assert issubclass(spec, tiles.tile), spec
    # magnitudes and unit values are real values
    assert issubclass(tiles.magnitude, tiles.real)
    assert issubclass(tiles.unit, tiles.real)
    # and a color channel is a unit value
    assert issubclass(tiles.channel, tiles.unit)
    # complex values are not real ones, nor the other way around
    assert not issubclass(tiles.complex, tiles.real)
    assert not issubclass(tiles.real, tiles.complex)
    # and each has a family of its own, under the tiles
    assert tiles.real.pyre_family() == "pyre.viz.tiles.real"
    assert tiles.channel.pyre_family() == "pyre.viz.tiles.channel"

    # a factory whose slots are typed by refinements
    class Scale(pyre.flow.factory, family="tests.pyre.viz.scale"):
        """
        Map real values onto unit ones
        """

        # the input
        signal = tiles.real.input()
        # and the output
        scaled = tiles.unit.output()

    # make one
    scale = Scale(name="scale")
    # its slots are typed by the refinements
    assert [trait.name for trait in Scale.pyre_inputTraits] == ["signal"]
    assert [trait.name for trait in Scale.pyre_outputTraits] == ["scaled"]
    assert Scale.pyre_trait(alias="signal").protocol is tiles.real
    assert Scale.pyre_trait(alias="scaled").protocol is tiles.unit

    # a tile on the heap
    signal = tiles.heap()(name="signal")
    # binds to the input that expects real values
    scale.signal = signal
    # and is there
    assert scale.signal is signal
    # as does another one to the output that expects unit values
    scaled = tiles.heap()(name="scaled")
    scale.scaled = scaled
    assert scale.scaled is scaled

    # the components of the amplitude pipeline type their slots by the specifications, in order
    stages = [
        # complex samples to magnitudes
        (pyre.viz.operators.amplitude, {"signal": tiles.complex, "amplitude": tiles.magnitude}),
        # reals to unit values
        (pyre.viz.normalizers.parametric, {"signal": tiles.real, "normalized": tiles.unit}),
        # unit values to color channels
        (
            pyre.viz.colormaps.gray,
            {
                "data": tiles.unit,
                "red": tiles.channel,
                "green": tiles.channel,
                "blue": tiles.channel,
            },
        ),
        # color channels to an image
        (
            pyre.viz.encoders.bmp,
            {
                "red": tiles.channel,
                "green": tiles.channel,
                "blue": tiles.channel,
                "image": pyre.viz.image,
            },
        ),
    ]
    # go through them
    for foundry, slots in stages:
        # get the component
        component = foundry()
        # check each slot
        for slot, spec in slots.items():
            # against its specification
            assert component.pyre_trait(alias=slot).protocol is spec, (component, slot)

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
