#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test():
    """
    Check that the hdf5 handles the bindings hand out die with the python objects that carry
    them: a handle that outlives its object keeps the file it belongs to open for the life of
    the process, no matter what the client does with the file itself
    """
    # get the bindings
    from pyre.extensions import libh5

    # for a scratch path and its cleanup, and to force collection
    import gc
    import os

    # a scratch data product
    uri = "h5_ext_handles.h5"
    # make sure a stale one is not lying around
    if os.path.exists(uri):
        os.remove(uri)

    # make the file
    f = libh5.File(uri=uri, mode="w")
    # with a group
    group = f.create(path="group")
    # and a couple of datasets in it
    space = libh5.DataSpace(shape=[4, 4])
    group.create(path="one", type=libh5.types.native.double, space=space)
    group.create(path="two", type=libh5.types.native.int32, space=space)
    # let go of everything but the file
    del group, space
    gc.collect()
    # so the file itself is the only thing it has open
    assert f.handles() == {"file": 1}

    # the ways to get at an object of the file, each of which hands back a fresh handle
    recipes = {
        "a group from the file, by path": lambda: f.get("group"),
        "a dataset from the file, by path": lambda: f.get("group/one"),
        "a dataset from a group, by name": lambda: f.get("group").get("one"),
        "a dataset from a group, by index": lambda: f.get("group").get(0),
        "the type of a dataset": lambda: f.get("group/one").type,
        "the space of a dataset": lambda: f.get("group/one").space,
        "the creation properties of a dataset": lambda: f.get("group/one").dcpl,
        "the access properties of a dataset": lambda: f.get("group/one").dapl,
        "the access properties of the file": lambda: f.fapl,
        "the creation properties of the file": lambda: f.fcpl,
    }
    # go through them
    for label, recipe in recipes.items():
        # make the object
        thing = recipe()
        # its handle is alive
        hid = thing.hid
        assert libh5.valid(hid), label
        # let go of it
        del thing
        gc.collect()
        # the handle is gone
        assert not libh5.valid(hid), f"{label}: the handle outlived its object"
        # and the file is back to having nothing but itself open
        assert f.handles() == {"file": 1}, f"{label}: {f.handles()}"

    # a walk over everything in the file, the way a client that explores a product does
    members = [f.get("group").get(index) for index in range(len(f.get("group")))]
    # while they are held, the file knows about them
    assert f.handles() == {"file": 1, "dataset": 2}
    # and when they go
    del members
    gc.collect()
    # so do their handles
    assert f.handles() == {"file": 1}

    # clean up
    del f
    gc.collect()
    os.remove(uri)

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
