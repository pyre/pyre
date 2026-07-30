// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// support
#include <cassert>
// for the reference pattern
#include <cstring>
// get the memory package
#include <pyre/memory.h>


// the storage strategy under test
using paged_t = pyre::memory::paged_t<pyre::memory::float64_t>;


// verify that poisoning a page materializes it and lays down a recognizable pattern,
// without disturbing the page state
int
main(int argc, char * argv[])
{
    // initialize the journal
    pyre::journal::init(argc, argv);
    // attribute whatever gets logged to this test
    pyre::journal::application("paged_poison");

    // a store with two pages of four cells each
    const paged_t store { 4, 2 };

    // poison the first page; this materializes it
    auto data = store.poison(0);
    // so the working set is one page
    assert((store.residents() == 1));
    // but the content is scaffolding, not a deposit: the state bits are untouched
    assert((!store.valid(0)));
    assert((store.clean(0)));

    // build the reference cell: a double whose every byte carries the pattern
    paged_t::value_type reference;
    // by scribbling it the same way
    std::memset(&reference, 0xdb, sizeof(reference));
    // every cell of the page carries the pattern, bit for bit
    for (paged_t::cell_count_type cell = 0; cell < store.pageCells(); ++cell) {
        // compare the bytes, since the pattern need not be a comparable number
        assert((std::memcmp(&data[cell], &reference, sizeof(reference)) == 0));
    }

    // a write covers the pattern in its cell
    data[1] = 42.0;
    assert((data[1] == 42.0));
    // and leaves it intact everywhere else
    assert((std::memcmp(&data[0], &reference, sizeof(reference)) == 0));

    // all done
    return 0;
}


// end of file
