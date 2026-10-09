#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that the protocols of the amplitude pipeline declare the slots every one of their components
must have, under the names the c++ factories use, and that the components remain compatible with
them, a slot of a component that refines the specification of its protocol included
"""


def test():
    # support
    import pyre

    # the specifications
    tiles = pyre.viz.tiles
    # the building block of the unary operators
    from pyre.viz.protocols.Unary import Unary

    # the protocols, with the slots they declare and the specifications of these slots
    protocols = [
        (Unary, {"signal": tiles.tile}),
        (pyre.viz.normalizer, {"signal": tiles.real, "normalized": tiles.unit}),
        (
            pyre.viz.colormap,
            {"red": tiles.channel, "green": tiles.channel, "blue": tiles.channel},
        ),
        (
            pyre.viz.encoder,
            {
                "red": tiles.channel,
                "green": tiles.channel,
                "blue": tiles.channel,
                "image": pyre.viz.raster,
            },
        ),
    ]
    # go through them
    for protocol, slots in protocols:
        # the slots the protocol declares: its facilities typed by a specification, by name
        traits = {
            trait.name: trait
            for trait in protocol.pyre_facilities()
            if issubclass(trait.protocol, pyre.flow.specification)
        }
        # must be the slots
        assert set(traits) == set(slots), (protocol, set(traits))
        # each typed by its specification
        for name, spec in slots.items():
            # check
            assert traits[name].protocol is spec, (protocol, name)

    # the components of the amplitude pipeline, with the protocol each implements
    components = [
        # whose input refines the specification of the protocol's
        (pyre.viz.operators.amplitude, Unary),
        (pyre.viz.normalizers.parametric, pyre.viz.normalizer),
        (pyre.viz.colormaps.gray, pyre.viz.colormap),
        (pyre.viz.encoders.bmp, pyre.viz.encoder),
    ]
    # go through them
    for foundry, protocol in components:
        # get the component
        component = foundry()
        # it must be compatible with its protocol
        report = component.pyre_isCompatible(spec=protocol)
        # with nothing to report
        assert report.isClean, (component, [str(problem) for problem in report.incompatibilities])

    # every colormap promises the three color channels
    for name in ("gray", "hl", "hsb", "hsl", "oklch", "complex"):
        # get the colormap
        colormap = getattr(pyre.viz.colormaps, name)()
        # it must be compatible with the protocol
        assert colormap.pyre_isCompatible(spec=pyre.viz.colormap).isClean, name

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
