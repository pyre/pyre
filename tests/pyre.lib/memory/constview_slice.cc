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
using heap_t = pyre::memory::heap_t<double>;
using constview_t = pyre::memory::constview_t<double>;
using slice_t = pyre::memory::Slice<constview_t>;


// verify that a {Slice} iterates a read-only {constview_t}, named and nameless
int
main(int argc, char * argv[])
{
    // initialize the journal
    pyre::journal::init(argc, argv);
    pyre::journal::application("constview_slice");

    // the number of cells
    std::size_t cells = 1024ul;

    // a heap that owns the buffer and outlives every view over it
    heap_t block(cells);
    // set every cell to its own index
    for (std::size_t pos = 0; pos < cells; ++pos) {
        // store the value
        block[pos] = pos;
    }

    // the named client: a read-only view over the whole block
    constview_t view(block.data(), block.cells());
    // walk it from {begin} to {end}
    std::size_t visited = 0;
    for (slice_t cur(view, 0), stop(view, view.cells()); cur != stop; ++cur, ++visited) {
        // each cell should carry its index
        assert((*cur == visited));
    }
    // the walk should have terminated exactly at the end of the view
    assert((visited == cells));

    // the nameless client: a slice from {begin} on a temporary const view of the live block
    slice_t cur = [&block]() {
        // the view exists only for this expression
        return constview_t(block.data(), block.cells()).begin();
    }();
    // the temporary view is gone; the slice's own copy still reads the live block
    for (std::size_t pos = 0; pos < cells; ++pos, ++cur) {
        // every cell should carry its index
        assert((*cur == pos));
    }

    // all done
    return 0;
}


// end of file
