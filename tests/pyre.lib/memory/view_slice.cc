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
using view_t = pyre::memory::view_t<double>;
using slice_t = pyre::memory::Slice<view_t>;


// verify that a {Slice} iterates a {view_t}, named and nameless, including a strided view
int
main(int argc, char * argv[])
{
    // initialize the journal
    pyre::journal::init(argc, argv);
    pyre::journal::application("view_slice");

    // the number of cells
    std::size_t cells = 1024ul;

    // a heap that owns the buffer and outlives every view over it
    heap_t block(cells);

    // the named client: a dense view over the whole block
    view_t view(block.data(), block.cells());
    // fill the block through the view
    for (std::size_t pos = 0; pos < cells; ++pos) {
        // each cell gets its own index
        view[pos] = pos;
    }
    // walk the view from {begin} to {end}
    std::size_t visited = 0;
    for (slice_t cur(view, 0), stop(view, view.cells()); cur != stop; ++cur, ++visited) {
        // each cell should carry its index
        assert((*cur == visited));
    }
    // the walk should have terminated exactly at the end of the view
    assert((visited == cells));

    // mutate the block through a view slice
    for (slice_t cur(view, 0), stop(view, view.cells()); cur != stop; ++cur) {
        // bump every cell in place
        *cur += 1;
    }
    // and confirm the writes are visible in the backing heap
    for (std::size_t pos = 0; pos < cells; ++pos) {
        // read back through the block itself
        assert((block[pos] == pos + 1));
    }

    // a strided view visits every other cell of the block
    view_t strided(block.data(), block.cells() / 2, 2);
    // walk it and confirm the stride is honored
    std::size_t hops = 0;
    for (slice_t cur(strided, 0), stop(strided, strided.cells()); cur != stop; ++cur, ++hops) {
        // cell {hops} of the strided view is cell {2*hops} of the block
        assert((*cur == 2 * hops + 1));
    }
    // and it should have covered half the block
    assert((hops == cells / 2));

    // the nameless client: a slice from {begin} on a temporary view of the still-live block
    slice_t cur = [&block]() {
        // the view exists only for this expression, but the block it refers to does not
        return view_t(block.data(), block.cells()).begin();
    }();
    // the temporary view is gone; the slice's own copy still points at the live block
    for (std::size_t pos = 0; pos < cells; ++pos, ++cur) {
        // the block was bumped once, so each cell carries its index plus one
        assert((*cur == pos + 1));
    }

    // all done
    return 0;
}


// end of file
