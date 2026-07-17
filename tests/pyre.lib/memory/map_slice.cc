// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// get the memory
#include <pyre/memory.h>
// support
#include <cassert>


// type aliases
using map_t = pyre::memory::map_t<double>;
using slice_t = pyre::memory::Slice<map_t>;


// verify that a {Slice} iterates a file-backed {map_t}, named and nameless
int
main(int argc, char * argv[])
{
    // initialize the journal
    pyre::journal::init(argc, argv);
    pyre::journal::application("map_slice");

    // the number of cells
    std::size_t cells = 1024ul;

    // the named client: a fresh file-backed block that outlives its iterators
    map_t block("map_slice.dat", cells);
    // prime every cell with its own index
    for (std::size_t pos = 0; pos < cells; ++pos) {
        // set the value
        block[pos] = pos;
    }

    // slice the named block and walk it from {begin} to {end}
    std::size_t visited = 0;
    for (slice_t cur(block, 0), stop(block, block.cells()); cur != stop; ++cur, ++visited) {
        // each cell should carry its index
        assert((*cur == visited));
    }
    // the walk should have terminated exactly at the end of the block
    assert((visited == cells));

    // mutate the block through a slice
    for (slice_t cur(block, 0), stop(block, block.cells()); cur != stop; ++cur) {
        // triple every cell in place
        *cur *= 3;
    }
    // and confirm the writes landed in the mapping
    for (std::size_t pos = 0; pos < cells; ++pos) {
        // read back through the block itself
        assert((block[pos] == 3.0 * pos));
    }

    // the nameless client: a slice over a temporary map of the same file; the shared {FileMap}
    // handle keeps the mapping alive after the temporary map is gone
    slice_t cur = []() {
        // open the existing file for writing, but only for this expression
        return slice_t(map_t("map_slice.dat", true), 0);
    }();
    // the temporary map is gone; the slice must still read the mapping it kept alive
    for (std::size_t pos = 0; pos < cells; ++pos, ++cur) {
        // every cell should carry its tripled index
        assert((*cur == 3.0 * pos));
    }

    // all done
    return 0;
}


// end of file
