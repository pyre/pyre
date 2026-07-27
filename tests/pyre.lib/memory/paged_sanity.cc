// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// get the memory
#include <pyre/memory.h>
// support
#include <cassert>


// type alias
using paged_t = pyre::memory::paged_t<double>;


// verify that a fresh paged store reports its geometry correctly and owns nothing
int
main(int argc, char * argv[])
{
    // initialize the journal
    pyre::journal::init(argc, argv);
    pyre::journal::application("paged_sanity");
    // make a channel
    pyre::journal::debug_t channel("pyre.memory.paged");

    // the geometry: a few pages of a few cells each
    paged_t::cell_count_type pageCells = 6;
    paged_t::cell_count_type pages = 4;
    // make a store
    paged_t store(pageCells, pages);
    // show me
    channel << store.uri() << pyre::journal::endl(__HERE__);

    // the geometry is what i asked for
    assert((store.pageCells() == pageCells));
    assert((store.pages() == pages));
    // the full expanse counts every page at full size
    assert((store.cells() == pageCells * pages));
    // but nothing is resident yet
    assert((store.residents() == 0));
    // so the store occupies no memory
    assert((store.bytes() == 0));
    // and every page is blank: not there, holding nothing meaningful, in sync with nothing
    for (paged_t::cell_count_type page = 0; page < pages; ++page) {
        // not allocated
        assert((!store.resident(page)));
        // no content
        assert((!store.valid(page)));
        // and nothing to save
        assert((store.clean(page)));
    }

    // bring one page in
    auto data = store.reside(1);
    // it hands out an actual allocation
    assert((data != nullptr));
    // the page is now resident
    assert((store.resident(1)));
    // asking again is idempotent: same page, same address
    assert((store.reside(1) == data));
    // and the address is also available by name
    assert((store.page(1) == data));
    // exactly one page is in
    assert((store.residents() == 1));
    // and the footprint is exactly one page
    assert((store.bytes() == pageCells * sizeof(paged_t::value_type)));
    // residency says nothing about content
    assert((!store.valid(1)));
    // and the neighbors are untouched
    assert((!store.resident(0) && !store.resident(2) && !store.resident(3)));

    // all done
    return 0;
}


// end of file
