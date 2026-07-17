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
using slice_t = pyre::memory::Slice<heap_t>;


// verify that a {Slice} iterates a {heap_t}, for both named and nameless clients
int
main(int argc, char * argv[])
{
    // initialize the journal
    pyre::journal::init(argc, argv);
    pyre::journal::application("heap_slice");

    // the number of cells
    std::size_t cells = 1024ul;

    // the named client: a block that outlives its iterators
    heap_t block(cells);
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
        // double every cell in place
        *cur *= 2;
    }
    // and confirm the writes landed in the underlying block
    for (std::size_t pos = 0; pos < cells; ++pos) {
        // read back through the block itself
        assert((block[pos] == 2.0 * pos));
    }

    // the nameless client: a slice over a temporary heap whose buffer it alone keeps alive
    slice_t cur = [cells]() {
        // a block owned only within this scope
        heap_t tmp(cells);
        // prime it
        for (std::size_t pos = 0; pos < cells; ++pos) {
            // with a shifted value so we can tell it apart
            tmp[pos] = pos + 1;
        }
        // hand back a slice; owning the handle by value keeps the buffer alive past {tmp}
        return slice_t(tmp, 0);
    }();
    // the temporary is gone; the slice must still read the buffer it kept alive
    for (std::size_t pos = 0; pos < cells; ++pos, ++cur) {
        // every cell should carry its shifted index
        assert((*cur == pos + 1));
    }

    // all done
    return 0;
}


// end of file
