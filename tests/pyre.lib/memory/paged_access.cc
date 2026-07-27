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


// bring every page in, write to every cell, and read them all back
int
main(int argc, char * argv[])
{
    // initialize the journal
    pyre::journal::init(argc, argv);
    pyre::journal::application("paged_access");

    // the geometry
    paged_t::cell_count_type pageCells = 6;
    paged_t::cell_count_type pages = 4;
    // make a store
    paged_t store(pageCells, pages);

    // bring every page in
    for (paged_t::cell_count_type page = 0; page < pages; ++page) {
        // by asking for its address
        auto data = store.reside(page);
        // pages are separate allocations, so each one fills through its own base
        for (paged_t::cell_count_type cell = 0; cell < pageCells; ++cell) {
            // stamp the cell with its logical offset in the store
            data[cell] = static_cast<paged_t::value_type>(page * pageCells + cell);
        }
    }
    // everything is in
    assert((store.residents() == pages));

    // sweep the whole logical expanse
    for (paged_t::cell_count_type pos = 0; pos < store.cells(); ++pos) {
        // the stamp encodes the offset, so both access paths must find it
        assert((store[pos] == static_cast<paged_t::value_type>(pos)));
        // guarded and unguarded alike
        assert((store.at(pos) == static_cast<paged_t::value_type>(pos)));
    }

    // writing through the offset path must be visible through the page base
    store[7] = 42;
    // page 1, cell 1, given six cells per page
    assert((store.page(1)[1] == 42));

    // a copy of the store is a view of the same pages, not a fresh store
    paged_t copy = store;
    // it sees the same content
    assert((copy[7] == 42));
    // and state changes made through one handle are visible through the other
    copy.validate(0);
    // both agree
    assert((store.valid(0)));

    // all done
    return 0;
}


// end of file
