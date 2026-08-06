// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// support
#include <cassert>
// get the memory package
#include <pyre/memory.h>


// the storage strategy under test
using paged_t = pyre::memory::paged_t<pyre::memory::float64_t>;


// verify that releasing a page returns it to the never-touched state, and that shared handles
// extend the life of its block
int
main(int argc, char * argv[])
{
    // initialize the journal
    pyre::journal::init(argc, argv);
    // attribute whatever gets logged to this test
    pyre::journal::application("paged_release");

    // a store with two pages of four cells each
    const paged_t store { 4, 2 };

    // bring the first page in
    auto data = store.reside(0);
    // fill it with something recognizable
    for (paged_t::cell_count_type cell = 0; cell < store.pageCells(); ++cell) {
        // stamp each cell with its own ordinal
        data[cell] = static_cast<paged_t::value_type>(cell);
    }
    // declare the deposit and go through a full save cycle
    store.validate(0);
    store.taint(0);
    store.flush(0);
    // the working set is one page
    assert((store.residents() == 1));

    // share ownership of the block before letting go
    auto handle = store.handle(0);
    // let the page go; it is clean, so this draws no complaint
    store.release(0);

    // the page is back in the never-touched state
    assert((!store.resident(0)));
    // with no meaningful content
    assert((!store.valid(0)));
    // and nothing to save
    assert((store.clean(0)));
    // the store has forgotten it: the working set is empty
    assert((store.residents() == 0));
    // and so is the memory bill
    assert((store.bytes() == 0));

    // but the shared handle kept the block alive: the content is intact
    assert((handle[3] == 3.0));

    // touching the page again materializes a fresh block
    auto fresh = store.reside(0);
    // not the one the handle holds, which is still allocated
    assert((fresh != handle.get()));

    // all done
    return 0;
}


// end of file
