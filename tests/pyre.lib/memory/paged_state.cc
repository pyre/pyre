// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// get the memory
#include <pyre/memory.h>
// support
#include <cassert>
#include <vector>


// type alias
using paged_t = pyre::memory::paged_t<double>;


// walk a page through its lifecycle and verify a writer can find its dirty pages
int
main(int argc, char * argv[])
{
    // initialize the journal
    pyre::journal::init(argc, argv);
    pyre::journal::application("paged_state");

    // the geometry
    paged_t::cell_count_type pageCells = 6;
    paged_t::cell_count_type pages = 4;
    // make a store
    paged_t store(pageCells, pages);

    // bring a page in
    store.reside(2);
    // a fresh page holds nothing meaningful and diverges from nothing
    assert((store.resident(2) && !store.valid(2) && store.clean(2)));

    // deposit content, the way a reader that just filled the page from its source would
    store.validate(2);
    // the content is now meaningful, and still in sync with the source
    assert((store.valid(2) && store.clean(2)));

    // write to the page, the way a client that computed new values would
    store.taint(2);
    // the content diverges from the source, and is still meaningful
    assert((store.valid(2) && !store.clean(2)));

    // save it, the way a writer that just persisted the page would
    store.flush(2);
    // back in sync
    assert((store.valid(2) && store.clean(2)));
    // and validity survived the whole cycle: flushing never takes the content away
    assert((store.valid(2)));

    // now the writer's workflow: touch a few pages
    for (auto page : { 0l, 3l }) {
        // bring each one in
        store.reside(page);
        // put content in it
        store.validate(page);
        // and modify it
        store.taint(page);
    }
    // scan the store for the pages that need saving
    std::vector<paged_t::cell_count_type> dirty;
    // by checking each page
    for (paged_t::cell_count_type page = 0; page < store.pages(); ++page) {
        // for divergence from the backing store
        if (store.resident(page) && !store.clean(page)) {
            // and collecting the ones that have drifted
            dirty.push_back(page);
        }
    }
    // the scan finds exactly the pages the writer touched
    assert((dirty == std::vector<paged_t::cell_count_type> { 0, 3 }));

    // all done
    return 0;
}


// end of file
