#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test():
    """
    Exercise the file access property list: the settings that govern how a file is reached,
    which apply on every open rather than once at creation
    """
    # get the bindings
    from pyre.extensions import libh5

    # for a scratch path and its cleanup
    import os

    # a scratch data product
    uri = "h5_ext_fapl.h5"
    # make sure a stale one is not lying around
    if os.path.exists(uri):
        os.remove(uri)

    # a fresh file access property list
    fapl = libh5.properties.fapl()

    # objects are not aligned, by default: any position will do
    assert fapl.alignment == (1, 1)
    # a product headed for a parallel filesystem lands its larger objects on boundaries
    fapl.alignment = (4096, 4096)
    assert fapl.alignment == (4096, 4096)

    # the sieve buffer gathers small writes to contiguous datasets
    assert fapl.sieveBufferSize > 0
    # and it is ours to size
    fapl.sieveBufferSize = 128 * 1024
    assert fapl.sieveBufferSize == 128 * 1024

    # the caches, as {(metadata elements, chunk slots, chunk bytes, preemption)}; these are
    # the defaults a dataset access property list overrides one dataset at a time
    elements, slots, bytes, w0 = fapl.cache
    # a workflow that sweeps large chunks wants room for more of them
    fapl.cache = (elements, slots, 64 * 1024 * 1024, w0)
    assert fapl.cache == (elements, slots, 64 * 1024 * 1024, w0)

    # what becomes of a file closed while objects in it are still open
    assert fapl.closeDegree == libh5.CloseDegree.default
    # ask for the handle to survive until the last object is done with it
    fapl.closeDegree = libh5.CloseDegree.strong
    assert fapl.closeDegree == libh5.CloseDegree.strong

    # the file format versions the library may use; {latest} is not a fixed point, it means
    # whatever the library we were built against considers newest, so reading the bound
    # back reports the concrete version it resolved to rather than the request
    fapl.libverBounds = (libh5.LibVersion.earliest, libh5.LibVersion.latest)
    low, high = fapl.libverBounds
    # the low bound is what we asked for
    assert low == libh5.LibVersion.earliest
    # and the high bound is at least as new as the oldest named format
    assert high >= libh5.LibVersion.v18

    # pinning the format keeps older libraries able to read what we write
    fapl.libverBounds = (libh5.LibVersion.earliest, libh5.LibVersion.v18)
    assert fapl.libverBounds == (libh5.LibVersion.earliest, libh5.LibVersion.v18)

    # make a file with it
    f = libh5.File(uri=uri, mode="w", fapl=fapl)
    # and put something in it, so the file is worth reading back
    f.create(path="group")

    # all done
    return


# main
if __name__ == "__main__":
    # drive
    test()


# end of file
