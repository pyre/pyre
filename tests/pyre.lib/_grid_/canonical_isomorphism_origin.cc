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
using canonical_t = pyre::grid::canonical_t<3>;
// and its parts
using shape_t = canonical_t::shape_type;
using index_t = canonical_t::index_type;
using order_t = canonical_t::order_type;


// check that a layout can undo its own packing
// {offset} and {index} are the two directions of the same isomorphism, so sending an index to
// memory and reading it back must return the index we started with, for every cell the layout
// addresses
static auto
mapsBothWays(const canonical_t & packing, pyre::journal::debug_t & channel) -> bool
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
        // the trip out and back must be the identity
        if (!(recovered == idx)) {
            // say which cell was lost and what came back instead
            channel << pyre::journal::at() << "  " << idx << " -> " << offset << " -> "
                    << recovered << "  <-- lost" << pyre::journal::newline;
            // and remember that this layout is broken
            sound = false;
        }
    }
    // report
    return sound;
}


// verify that the packing isomorphism survives an origin anywhere in the index space
int
main(int argc, char * argv[])
{
    // initialize the journal
    pyre::journal::init(argc, argv);
    // attribute whatever gets logged to this test
    pyre::journal::application("canonical_isomorphism_origin");
    // make a channel
    pyre::journal::debug_t channel("pyre.grid.canonical");

    // give every axis a different extent, so that a mistaken decomposition cannot be masked by
    // the extents happening to line up
    constexpr shape_t shape { 2, 3, 4 };

    // the anchor of a layout is a signed index, so each axis may sit below the origin of the
    // index space, on it, or above it; these three representatives cover the cases, and the
    // negative one is the interesting one because integer division truncates toward zero
    constexpr index_t::value_type anchors[] = { -2, 0, 3 };

    // room for the axis labels we will permute
    order_t::storage_type labels {};
    // start from the identity, which packs the leading axis fastest
    for (canonical_t::size_type axis = 0; axis < canonical_t::rank(); ++axis) {
        labels[axis] = axis;
    }

    // the packing order and the placement of the anchor are independent choices, so exercise
    // every combination of the two rather than trusting that they do not interact
    do {
        // adopt this permutation as the packing order
        const order_t order { labels };
        // and try it against every placement of the anchor along the first axis
        for (auto i : anchors) {
            // the second
            for (auto j : anchors) {
                // and the third, which together cover the sign patterns, mixed ones included
                for (auto k : anchors) {
                    // anchor the layout here
                    const index_t origin { i, j, k };
                    // lay out a grid with this anchor and this packing order
                    const canonical_t packing { shape, origin, order };
                    // name the case on trial, so that a failure can be attributed
                    channel << pyre::journal::at() << "order: " << order << ", origin: " << origin
                            << pyre::journal::newline;
                    // and check that the layout can undo its own packing
                    assert(mapsBothWays(packing, channel));
                }
            }
        }
    } while (std::next_permutation(labels.begin(), labels.end()));

    // flush the trace
    channel << pyre::journal::endl;

    // all done
    return 0;
}


// end of file
