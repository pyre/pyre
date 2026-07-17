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
using constheap_t = pyre::memory::constheap_t<double>;
using slice_t = pyre::memory::Slice<constheap_t>;


// verify that a {Slice} iterates a read-only {constheap_t}, named and nameless
int
main(int argc, char * argv[])
{
    // initialize the journal
    pyre::journal::init(argc, argv);
    pyre::journal::application("constheap_slice");

    // the number of cells
    std::size_t cells = 1024ul;

    // a writable block to prime the data
    heap_t writable(cells);
    // set every cell to its own index
    for (std::size_t pos = 0; pos < cells; ++pos) {
        // store the value
        writable[pos] = pos;
    }

    // the named client: a read-only block borrowing the same buffer
    constheap_t block(writable.handle(), writable.cells());
    // walk it from {begin} to {end}
    std::size_t visited = 0;
    for (slice_t cur(block, 0), stop(block, block.cells()); cur != stop; ++cur, ++visited) {
        // each cell should carry its index
        assert((*cur == visited));
    }
    // the walk should have terminated exactly at the end of the block
    assert((visited == cells));

    // the nameless client: a slice over a temporary const block sharing the same buffer
    slice_t cur = [&writable]() {
        // hand back a slice over a const block that exists only for this expression
        return slice_t(constheap_t(writable.handle(), writable.cells()), 0);
    }();
    // the temporary const block is gone; the slice must still read the shared buffer
    for (std::size_t pos = 0; pos < cells; ++pos, ++cur) {
        // every cell should carry its index
        assert((*cur == pos));
    }

    // all done
    return 0;
}


// end of file
