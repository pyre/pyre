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
using canonical_t = pyre::grid::canonical_t<3>;
// and its parts
using shape_t = canonical_t::shape_type;
using index_t = canonical_t::index_type;


// check that a layout can undo its own packing
// {offset} and {index} are the two directions of the same isomorphism, so sending an index to
// memory and reading it back must return the index we started with, for every cell the layout
// addresses
template <std::size_t N>
static auto
mapsBothWays(const pyre::grid::canonical_t<N> & packing, pyre::journal::debug_t & channel) -> bool
{
    // assume the layout is sound until a cell says otherwise
    auto sound = true;
    // go through every index the layout addresses
    for (auto it = packing.begin(); it != packing.end(); ++it) {
        // name the cell we are checking
        auto idx = *it;
        // send it to memory
        auto offset = packing.offset(idx);
        // and ask the layout where that landing spot came from
        auto recovered = packing.index(offset);
        // show me
        channel << "  " << idx << " -> " << offset << " -> " << recovered;
        // the trip out and back must be the identity
        if (!(recovered == idx)) {
            // say so
            channel << "  <-- lost";
            // and remember that this layout is broken
            sound = false;
        }
        // move on to the next cell
        channel << pyre::journal::newline;
    }
    // flush the trace
    channel << pyre::journal::endl(__HERE__);
    // report
    return sound;
}


// verify that the packing isomorphism is invertible
int
main(int argc, char * argv[])
{
    // initialize the journal
    pyre::journal::init(argc, argv);
    // attribute whatever gets logged to this test
    pyre::journal::application("canonical_isomorphism");
    // make a channel
    pyre::journal::debug_t channel("pyre.grid.canonical");

    // pick a shape
    constexpr shape_t shape { 2, 3, 4 };

    // a layout anchored at the origin is the simplest case
    channel << "at the origin:" << pyre::journal::endl;
    const canonical_t plain { shape };
    const auto plainMaps = mapsBothWays(plain, channel);

    // moving the origin puts the nudge to work, so the inverse has to undo that too
    channel << "away from the origin:" << pyre::journal::endl;
    const canonical_t shifted { shape, index_t { 1, 1, 1 } };
    const auto shiftedMaps = mapsBothWays(shifted, channel);

    // a sub box inherits the memory layout of its parent while carrying its own anchor, so it is
    // the first case where the two halves of the isomorphism have to agree about whose origin
    // they are speaking of
    channel << "a sub box:" << pyre::journal::endl;
    const auto tile = plain.box(index_t { 1, 1, 1 }, shape_t { 1, 2, 3 });
    const auto tileMaps = mapsBothWays(tile, channel);

    // a hyperplane pins the axes it drops and keeps the parent's strides for the ones it
    // survives with, so the recovered index must still name a cell of the slice
    channel << "a hyperplane:" << pyre::journal::endl;
    const auto plane = plain.slice<0, 2>(index_t { 0, 1, 0 });
    const auto planeMaps = mapsBothWays(plane, channel);

    // every layout above gets its say before the first failure stops us, so that one run of this
    // test names all of the broken cases rather than just the earliest one
    assert(plainMaps);
    assert(shiftedMaps);
    assert(tileMaps);
    assert(planeMaps);

    // all done
    return 0;
}


// end of file
