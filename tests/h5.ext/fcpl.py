#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test():
    """
    Exercise the file creation property list: the settings that are fixed when a file is
    made and cannot be revised afterwards
    """
    # get the bindings
    from pyre.extensions import libh5

    # the property namespace, which is where the records live
    p = libh5.properties

    # for a scratch path and its cleanup
    import os

    # a scratch data product
    uri = "h5_ext_fcpl.h5"
    # make sure a stale one is not lying around
    if os.path.exists(uri):
        os.remove(uri)

    # a fresh file creation property list
    fcpl = libh5.properties.fcpl()

    # the widths used to record positions and lengths; eight bytes each addresses more
    # than any product we will ever write
    assert (fcpl.sizes.offsets, fcpl.sizes.lengths) == (8, 8)

    # nothing is reserved at the front of the file, by default
    assert fcpl.userblock == 0
    # a file that another format has to carry reserves a block there; hdf5 requires it to
    # be a power of two, and at least 512 bytes
    fcpl.userblock = 1024
    assert fcpl.userblock == 1024

    # the free space strategy, as {(strategy, persist, threshold)}
    free = fcpl.filespaceStrategy
    # free space is not persisted across sessions, by default
    assert free.persist is False
    # ask for it to be, so a product that is revised repeatedly can reuse its own holes
    free.persist = True
    fcpl.filespaceStrategy = free
    assert fcpl.filespaceStrategy.persist is True

    # make a file with it
    f = libh5.File(uri=uri, mode="w", fcpl=fcpl)
    # and put something in it, so the file is worth reading back
    f.create(path="group")

    # all done
    return


# main
if __name__ == "__main__":
    # drive
    test()


# end of file
