#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test():
    """
    Exercise the raw data chunk cache: reading a compressed chunk a second time must be served
    from the cache rather than inflated again

    The library holds decompressed chunks in a per dataset cache, and consults it only on the
    path that hands over a whole chunk at once. That path is available when the destination
    has the same rank as the source. Describing the destination instead as a flat run of the
    same number of cells is accepted, and returns identical data, so nothing about the answer
    reveals the difference -- but the library must then scatter the chunk cell by cell, and it
    inflates the chunk again on every read no matter what is already in the cache. On a
    compressed product that is the difference between repeating a read in microseconds and
    repeating it in milliseconds, and it is invisible to any test that only checks the values
    """
    # get the bindings
    from pyre.extensions import libh5

    # for a scratch path, timing, and a buffer
    import os
    import time
    import array

    # a scratch data product
    uri = "read_chunk_cache.h5"
    # make sure a stale one is not lying around
    if os.path.exists(uri):
        os.remove(uri)

    # the layout: a raster of one chunk, big enough that inflating it is measurable
    chunk = [512, 512]
    cells = chunk[0] * chunk[1]

    # make the file
    f = libh5.File(uri=uri, mode="w")
    # describe the extent
    space = libh5.DataSpace(shape=chunk)
    # the creation properties: one chunk, compressed, so a read has real work to do
    dcpl = libh5.properties.dcpl()
    dcpl.chunk = chunk
    dcpl.addShuffle()
    dcpl.addDeflate(4)
    # make the dataset
    dataset = f.create(
        path="product", type=libh5.types.native.double, space=space, dcpl=dcpl
    )

    # fill it with something that does not compress, or the inflation costs nothing and there
    # is no difference left to detect. a regular sequence is crushed by shuffle and deflate
    # into a chunk that reinflates in microseconds; these are the low bits of a linear
    # congruential sequence, which are noise as far as a compressor is concerned, and the
    # sequence is fixed so the test measures the same work every time
    def noise():
        """
        Generate {cells} pseudo random values, deterministically
        """
        # a seed
        state = 0x2545F4914F6CDD1D
        # go through the cells
        for _ in range(cells):
            # advance the sequence
            state = (state * 6364136223846793005 + 1442695040888963407) % (2**64)
            # and hand back its low bits, which carry no pattern to exploit
            yield float(state & 0xFFFFFFFF)

    payload = array.array("d", noise())
    dataset.write(payload, libh5.types.native.double, [0, 0], chunk)
    # close, and let go of every handle into the file. the library reference counts its open
    # files: reopening one while a handle is still alive hands back the same file, chunk
    # cache and all, and the chunk this test just wrote would still be sitting in it. the
    # first read would then be served from the cache like every other, and the measurement
    # would compare a cache hit against a cache hit
    f.close()
    del dataset
    del f

    # open it again, with a cache with room to spare for the one chunk
    fapl = libh5.properties.fapl()
    fapl.cache = libh5.properties.Cache(
        fapl.cache.metadataElements, 521, 16 * cells * 8, 0.75
    )
    f = libh5.File(uri=uri, mode="r", fapl=fapl)
    dataset = f.dataset(path="product")

    # somewhere to put it
    buffer = array.array("d", bytes(cells * 8))

    # time a read
    def read():
        """
        Read the whole chunk and report how long it took, in milliseconds
        """
        # start the clock
        start = time.perf_counter()
        # pull the tile
        dataset.read(buffer, libh5.types.native.double, [0, 0], chunk)
        # and report
        return (time.perf_counter() - start) * 1000

    # the first read inflates the chunk
    first = read()
    # the ones after it must not: they are served from the cache
    repeats = [read() for _ in range(4)]

    # the data has to be right, whichever path delivered it
    assert buffer[0] == payload[0]
    assert buffer[cells // 2] == payload[cells // 2]
    assert buffer[cells - 1] == payload[cells - 1]

    # and a repeat must be far cheaper than an inflation. the margin is deliberately loose --
    # the measured ratio is around a hundred, and this asks for four -- because the point is
    # to catch a destination that silently loses the cache, not to police the timing
    best = min(repeats)
    assert best * 4 < first, (
        f"a repeated read cost {best:.3f}ms against {first:.3f}ms for the first, "
        f"which means the chunk was inflated again rather than taken from the cache"
    )

    # clean up
    f.close()

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
