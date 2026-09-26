#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test():
    """
    Exercise the tally of the page buffer, and the size of a file

    A paged file opened with a page buffer keeps the pages it reads in memory, and the buffer
    keeps count of what it was asked for and how often it had the page already. Two chunks
    that share a page have to show up as a miss followed by a hit, a tally that is started
    over has to read zero, and a file opened without a buffer has no tally to report at all.
    The chunks are read once each, since a chunk read twice is served by the chunk cache,
    which sits in front of the page buffer and never lets the second request reach it
    """
    # get the bindings
    from pyre.extensions import libh5

    # for a scratch path and a payload
    import os
    import array

    # a scratch data product
    uri = "page_buffer.h5"
    # make sure a stale one is not lying around
    if os.path.exists(uri):
        # by removing it
        os.remove(uri)

    # the layout: a small raster in chunks of a kilobyte, a quarter of a page; a chunk bigger
    # than a page goes around the buffer altogether
    extent = [64, 64]
    chunk = [8, 16]
    cells = chunk[0] * chunk[1]
    # the page size
    page = 4096

    # the creation properties of a paged file
    fcpl = libh5.properties.fcpl()
    # ask for the paged file space strategy
    free = fcpl.filespaceStrategy
    free.strategy = libh5.FilespaceStrategy.page
    fcpl.filespaceStrategy = free
    # with small pages
    fcpl.pageSize = page
    # make the file
    f = libh5.File(uri=uri, mode="w", fcpl=fcpl)
    # describe the extent
    space = libh5.DataSpace(shape=extent)
    # the creation properties: chunked
    dcpl = libh5.properties.dcpl()
    dcpl.chunk = chunk
    # make the dataset
    raster = f.create(path="raster", type=libh5.types.native.double, space=space, dcpl=dcpl)
    # something to write
    payload = array.array("d", (float(cell) for cell in range(cells)))
    # two neighboring chunks
    neighbors = [[0, 0], [8, 0]]
    # write them
    for origin in neighbors:
        # one after the other, so they are allocated side by side
        raster.write(payload, libh5.types.native.double, origin, chunk)
    # they share a page, which is what the rest of this relies on
    assert len({entry.address // page for entry in raster.chunkTable()}) == 1
    # the file was opened without a page buffer, so it has no tally, and nothing to reset
    assert f.pageBuffer is None
    assert f.resetPageBuffer() is False
    # done writing; the dataset keeps the file open for as long as it lives, and a file that is
    # still open is handed back as is when it is opened again, page buffer or not
    del raster
    # so let go of both
    f.close()

    # the access properties of a reader with a page buffer of a few pages
    fapl = libh5.properties.fapl()
    fapl.pageBufferSize = libh5.properties.PageBuffer(bytes=16 * page, metadata=0, raw=0)
    # open the file again
    f = libh5.File(uri=uri, mode="r", fapl=fapl)
    # the file is at least as big as the chunk it holds
    assert f.bytes >= cells * 8
    # get the dataset
    raster = f.dataset(path="raster")
    # start the tally over, so opening the file does not count
    assert f.resetPageBuffer() is True
    # and check that it did
    stats = f.pageBuffer
    assert stats.accesses == [0, 0]
    assert stats.hits == [0, 0]

    # room for a chunk
    scratch = array.array("d", bytes(cells * 8))
    # read the first chunk
    raster.read(scratch, libh5.types.native.double, neighbors[0], chunk)
    # the tally now shows raw data traffic
    first = f.pageBuffer
    # the buffer was asked for raw data
    assert first.accesses[1] == 1
    # and had to go to the file for its page
    assert first.misses[1] == 1
    # read its neighbor
    raster.read(scratch, libh5.types.native.double, neighbors[1], chunk)
    # this time the page was at hand
    second = f.pageBuffer
    # so the request was a hit, and nothing more was fetched
    assert second.hits[1] == first.hits[1] + 1
    assert second.misses[1] == first.misses[1]
    # nothing went around the buffer
    assert second.bypasses[1] == 0

    # clean up
    f.close()

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
