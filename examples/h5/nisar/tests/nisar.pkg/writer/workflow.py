#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
The value binding playground: a producer workflow over the GSLC product, written the way we
want it to read when the writer design lands.

This driver is the shared whiteboard for the value binding walkthrough. It mirrors the
setup of {gslc.py} — spec, shapes, assembler — and then walks the producer lifecycle we
mapped: interrogate the unbound raster, allocate and deposit through the factories, realize
the product, flush, and continue. It is deliberately excluded from the test suite while the
design is in flux — the exclusion also removes the named {mm} target, so run it with
{python3 workflow.py} from this directory.
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
    print(data)
    print(data.science)
    print(data.science.LSAR)
    spec._pyre_shapes.dump()

    # the frontier: everything below this line is the conversation
    #
    # the mapped lifecycle, for orientation:
    #   1. unbound work: get hold of a raster, interrogate it, allocate through its
    #      factories, deposit; the shape gate refuses allocation when extents are unknown
    #   2. realization: the product reaches the file; the raster acquires its on-disk
    #      counterpart mid-workflow and previous materializations stay live
    #   3. bound work: flush what diverged, open other windows, keep going

    # all done
    return


# main
if __name__ == "__main__":
    # drive
    test()


# end of file
