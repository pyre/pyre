// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// support
#include <cassert>
#include <algorithm>
// get the grid
#include <pyre/_grid_.h>


// the packing strategy under test
using symmetric_t = pyre::grid::symmetric_t<3>;
// and its parts
using shape_t = symmetric_t::shape_type;
using index_t = symmetric_t::index_type;


// verify the symmetric packing: an index and every permutation of its coordinates share one
// stored cell, so a symmetric object reads the same value whichever way its indices are ordered
int
main(int argc, char * argv[])
{
    // initialize the journal
    pyre::journal::init(argc, argv);
    // attribute whatever gets logged to this test
    pyre::journal::application("symmetric_sharing");
    // make a channel
    pyre::journal::debug_t channel("pyre.grid.symmetric");

    // a cube of dimension four
    constexpr shape_t shape { 4, 4, 4 };
    // lay it out symmetrically
    constexpr symmetric_t packing { shape };

    // the footprint is the number of entries in one triangular half; for a rank three cube of
    // dimension four that is the tetrahedral number, twenty
    static_assert(packing.cells() == 20);

    // every permutation of a fixed set of coordinates lands on the same cell
    constexpr index_t base { 1, 2, 3 };
    static_assert(packing.offset(base) == packing.offset(index_t { 1, 3, 2 }));
    static_assert(packing.offset(base) == packing.offset(index_t { 2, 1, 3 }));
    static_assert(packing.offset(base) == packing.offset(index_t { 2, 3, 1 }));
    static_assert(packing.offset(base) == packing.offset(index_t { 3, 1, 2 }));
    static_assert(packing.offset(base) == packing.offset(index_t { 3, 2, 1 }));

    // distinct sorted coordinates land on distinct cells
    static_assert(packing.offset({ 0, 0, 0 }) != packing.offset({ 1, 1, 1 }));
    static_assert(packing.offset({ 0, 1, 2 }) != packing.offset({ 0, 1, 3 }));

    // walk the whole box and check two invariants at once: every offset is a valid cell of the
    // stored half, and any two indices that are permutations of each other coincide
    for (auto it = packing.begin(); it != packing.end(); ++it) {
        // name the cell
        auto idx = *it;
        // where it lands
        auto off = packing.offset(idx);
        // show me
        channel << pyre::journal::at() << "  " << idx << " -> " << off << pyre::journal::newline;
        // the offset addresses a genuine stored cell
        assert((off >= 0 && off < packing.cells()));
        // sorting the coordinates cannot change where the index lands
        auto twin = idx;
        std::sort(twin.begin(), twin.end());
        assert((packing.offset(twin) == off));
    }
    // flush the trace
    channel << pyre::journal::endl;

    // the stored offsets are exactly {0 .. cells-1}, each hit once by its sorted representative:
    // recover the index a stored offset came from, and confirm it maps back to that offset
    for (symmetric_t::difference_type off = 0; off < packing.cells(); ++off) {
        // the representative index for this cell
        auto idx = packing.index(off);
        // must map forward to the very offset we started from
        assert((packing.offset(idx) == off));
    }

    // all done
    return 0;
}


// end of file
