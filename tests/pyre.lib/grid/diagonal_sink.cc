// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// support
#include <cassert>
// get the grid
#include <pyre/grid.h>


// the packing strategy under test
using diagonal_t = pyre::grid::diagonal_t<3>;
// and its parts
using shape_t = diagonal_t::shape_type;
using index_t = diagonal_t::index_type;


// verify the diagonal packing: the diagonal cells are distinct, everything off diagonal shares
// a single sink cell, and that sink is real allocated memory the footprint accounts for
int
main(int argc, char * argv[])
{
    // initialize the journal
    pyre::journal::init(argc, argv);
    // attribute whatever gets logged to this test
    pyre::journal::application("diagonal_sink");
    // make a channel
    pyre::journal::debug_t channel("pyre.grid.diagonal");

    // a cube whose diagonal has four cells
    constexpr shape_t shape { 4, 4, 4 };
    // lay it out as a diagonal
    constexpr diagonal_t packing { shape };

    // the memory footprint is the four diagonal cells plus the one shared sink
    static_assert(packing.cells() == 5);

    // each diagonal index lands on its own cell, at its position along the diagonal
    static_assert(packing.offset({ 0, 0, 0 }) == 0);
    static_assert(packing.offset({ 1, 1, 1 }) == 1);
    static_assert(packing.offset({ 2, 2, 2 }) == 2);
    static_assert(packing.offset({ 3, 3, 3 }) == 3);

    // every off diagonal index, however it strays, lands on the one sink cell just past the
    // diagonal; this is the contract a diagonal object reads its implied zeros through
    static_assert(packing.offset({ 0, 1, 0 }) == 4);
    static_assert(packing.offset({ 1, 0, 2 }) == 4);
    static_assert(packing.offset({ 3, 3, 0 }) == 4);
    static_assert(packing.offset({ 0, 0, 3 }) == 4);

    // walk the whole box and confirm the split: on diagonal indices are distinct and below the
    // sink, off diagonal indices all coincide on it
    for (auto it = packing.begin(); it != packing.end(); ++it) {
        // name the cell
        auto idx = *it;
        // where it lands
        auto off = packing.offset(idx);
        // show me
        channel << pyre::journal::at() << "  " << idx << " -> " << off << pyre::journal::newline;
        // whether this index is actually on the diagonal
        const bool onDiagonal = (idx[0] == idx[1]) && (idx[1] == idx[2]);
        // a diagonal index sits in its own cell, strictly before the sink
        // an off diagonal one sits exactly on the sink
        assert((onDiagonal ? off < packing.cells() - 1 : off == packing.cells() - 1));
    }
    // flush the trace
    channel << pyre::journal::endl;

    // a stored offset recovers the diagonal index it names
    static_assert(packing.index(2) == index_t { 2, 2, 2 });

    // all done
    return 0;
}


// end of file
