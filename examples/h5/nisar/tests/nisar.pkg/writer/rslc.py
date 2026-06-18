#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Emit a real RSLC file with programmatically controlled raster shapes and verify the result.

In radar geometry the azimuth extent is shared across the frequency sub-bands, declared on
the {swaths} group, while the range extent is per-frequency. Setting the shared azimuth and a
single frequency's range materializes that sub-band at the resolved extents and drops the
other, whose range was never set.
"""


# the driver
def test():
    # support
    import os
    import pyre
    from nisar.schema.rslc import rslc

    # build the product specification
    spec = rslc(name="root")

    # control the shapes: the shared azimuth extent, and the range extent for {frequencyA}
    # only; {frequencyB}'s range dimension is deliberately left unset
    spec._pyre_shapes["RSLC.swaths.nlines"] = 8
    spec._pyre_shapes["RSLC.swaths.frequencyA.nsamples"] = 5

    # shape the in-memory product
    data = pyre.h5.api.assembler().visit(descriptor=spec)

    # write it to a scratch file
    uri = "/tmp/nisar_rslc_write_test.h5"
    # starting from a clean slate
    if os.path.exists(uri):
        os.unlink(uri)
    # persist
    pyre.h5.write(uri=uri, data=data)

    # read it back by inference, so we are inspecting the actual on-disk structure
    recovered = pyre.h5.read(uri=uri)
    # the L-band swaths group
    swaths = "science/LSAR/RSLC/swaths"

    # the shared azimuth coordinate axis resolved to the value we set
    assert recovered._pyre_find(f"{swaths}/zeroDopplerTime").shape == [8]

    # {frequencyA} materialized; its polarization channels are sized from the shared azimuth
    # extent and the frequency's own range extent
    for pol in ("HH", "HV", "VH", "VV"):
        # the raster is present at the resolved extents
        assert recovered._pyre_find(f"{swaths}/frequencyA/{pol}").shape == [8, 5]
    # as is the per-frequency range coordinate axis
    assert recovered._pyre_find(f"{swaths}/frequencyA/slantRange").shape == [5]

    # {frequencyB}, whose range dimension was never set, is absent from the file: navigating to
    # it fails because the parent never created the sub-band
    try:
        recovered._pyre_find(f"{swaths}/frequencyB")
        assert False, "expected the unresolved frequency sub-band to be absent"
    except KeyError:
        pass

    # clean up
    os.unlink(uri)

    # all done
    return


# main
if __name__ == "__main__":
    # drive
    test()


# end of file
