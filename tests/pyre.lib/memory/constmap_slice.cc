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
using constmap_t = pyre::memory::constmap_t<double>;
using slice_t = pyre::memory::Slice<constmap_t>;


// verify that a {Slice} iterates a read-only file-backed {constmap_t}, named and nameless
int
main(int argc, char * argv[])
{
    // initialize the journal
    pyre::journal::init(argc, argv);
    pyre::journal::application("constmap_slice");

    // the number of cells
    std::size_t cells = 1024ul;

    // prime a file through a writable map that closes at the end of this scope
    {
        // create the file-backed block
        map_t primer("constmap_slice.dat", cells);
        // set every cell to its own index
        for (std::size_t pos = 0; pos < cells; ++pos) {
            // store the value
            primer[pos] = pos;
        }
    }

    // the named client: a read-only map over the existing file
    constmap_t block("constmap_slice.dat");
    // walk it from {begin} to {end}
    std::size_t visited = 0;
    for (slice_t cur(block, 0), stop(block, block.cells()); cur != stop; ++cur, ++visited) {
        // each cell should carry its index
        assert((*cur == visited));
    }
    // the walk should have terminated exactly at the end of the block
    assert((visited == cells));

    // the nameless client: a slice over a temporary read-only map of the same file; the shared
    // {FileMap} handle keeps the mapping alive after the temporary map is gone
    slice_t cur = []() {
        // open the existing file read-only, but only for this expression
        return slice_t(constmap_t("constmap_slice.dat"), 0);
    }();
    // the temporary map is gone; the slice must still read the mapping it kept alive
    for (std::size_t pos = 0; pos < cells; ++pos, ++cur) {
        // every cell should carry its index
        assert((*cur == pos));
    }

    // all done
    return 0;
}


// end of file
