#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test():
    """
    Exercise the link creation and link access property lists: how names are laid down, and
    how they are followed
    """
    # get the bindings
    from pyre.extensions import libh5

    # for a scratch path and its cleanup
    import os

    # a scratch data product
    uri = "h5_ext_lcpl.h5"
    # make sure a stale one is not lying around
    if os.path.exists(uri):
        os.remove(uri)

    # a fresh link creation property list
    lcpl = libh5.properties.lcpl()

    # names are recorded as ascii, by default
    assert lcpl.charEncoding == libh5.CharacterSet.ascii
    # a product whose member names are not plain ascii says so
    lcpl.charEncoding = libh5.CharacterSet.utf8
    assert lcpl.charEncoding == libh5.CharacterSet.utf8

    # missing groups along a path are not created, by default
    assert lcpl.intermediateGroupCreation is False
    # ask for them to be
    lcpl.intermediateGroupCreation = True
    assert lcpl.intermediateGroupCreation is True

    # make a file
    f = libh5.File(uri=uri, mode="w")

    # without the property list, a path whose parents are missing cannot be laid down; with
    # it, one call creates the whole chain and hands back the deepest group
    deep = f.create(path="science/LSAR/GSLC/grids", lcpl=lcpl)
    # every group along the way is there
    assert "science" in f
    assert "LSAR" in f.get(path="science")
    assert "grids" in f.get(path="science/LSAR/GSLC")
    # and what came back is the last one
    assert deep is not None

    # datasets take the same treatment: the groups above one are created on demand
    space = libh5.DataSpace(shape=[4])
    f.create(
        path="science/LSAR/GSLC/metadata/orbit",
        type=libh5.types.native.double,
        space=space,
        lcpl=lcpl,
    )
    # so the group that was never asked for exists
    assert "metadata" in f.get(path="science/LSAR/GSLC")

    # a fresh link access property list
    lapl = libh5.properties.lapl()
    # it will follow a bounded number of links before calling it a cycle
    assert lapl.traversalLimit > 0
    # and that bound is ours to set
    lapl.traversalLimit = 8
    assert lapl.traversalLimit == 8

    # nothing is prepended to the filenames external links name, by default
    assert lapl.externalPrefix == ""
    # a product whose external targets have moved says where they went
    lapl.externalPrefix = "/data/granules"
    assert lapl.externalPrefix == "/data/granules"

    # all done
    return


# main
if __name__ == "__main__":
    # drive
    test()


# end of file
