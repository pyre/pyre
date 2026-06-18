#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Emit a real GSLC file with programmatically controlled raster shapes and verify the result.

In geocoded geometry both grid extents are per-frequency, declared on the {Grid} group, so a
sub-band materializes only once both of its dimensions are set. Sizing {frequencyA}'s grid
materializes it at the resolved extents and drops {frequencyB}, whose grid was never set.
"""


# the driver
def test():
    # support
    import pyre
    from nisar.schema.gslc import gslc

    # build the product specification
    spec = gslc(name="root")

    # control the shapes: both grid extents for {frequencyA} only; {frequencyB}'s grid is
    # deliberately left unset
    spec._pyre_shapes["GSLC.grids.frequencyA.nlines"] = 8
    spec._pyre_shapes["GSLC.grids.frequencyA.nsamples"] = 5

    # shape the in-memory product
    data = pyre.h5.api.assembler().visit(descriptor=spec)

    # write it to a product next to this driver; the suite cleans it before the run and on
    # {mm clean}, so the driver itself does no filesystem housekeeping
    uri = "gslc.h5"
    # persist
    pyre.h5.write(uri=uri, data=data)

    # read it back by inference, so we are inspecting the actual on-disk structure
    recovered = pyre.h5.read(uri=uri)
    # the L-band grids group
    grids = "science/LSAR/GSLC/grids"

    # {frequencyA} materialized; its polarization channels are sized from the per-frequency
    # grid extents, with rows along y and columns along x
    for pol in ("HH", "HV", "VH", "VV"):
        # the raster is present at the resolved extents
        assert recovered._pyre_find(f"{grids}/frequencyA/{pol}").shape == [8, 5]
    # the projected coordinate axes follow the grid: x spans the columns, y the rows
    assert recovered._pyre_find(f"{grids}/frequencyA/xCoordinates").shape == [5]
    assert recovered._pyre_find(f"{grids}/frequencyA/yCoordinates").shape == [8]

    # {frequencyB}, whose grid was never set, is absent from the file: navigating to it fails
    # because the parent never created the sub-band
    try:
        recovered._pyre_find(f"{grids}/frequencyB")
        assert False, "expected the unresolved frequency sub-band to be absent"
    except KeyError:
        pass

    # all done
    return


# main
if __name__ == "__main__":
    # drive
    test()


# end of file
