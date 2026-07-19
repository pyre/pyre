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
using canonical_t = pyre::grid::canonical_t<4>;
// and its parts
using shape_t = canonical_t::shape_type;
using order_t = canonical_t::order_type;


// walk a tightly packed layout and check that it hands out its cells in memory order
// a packing order lists the axes from the fastest varying to the slowest, so a traversal that
// honors it steps through consecutive cells of the memory block; anything else means the
// traversal disagrees with the layout it is supposed to be walking
static auto
visitsInMemoryOrder(const canonical_t & packing, pyre::journal::debug_t & channel) -> bool
{
    // the offset the next visit should land on
    canonical_t::difference_type expected = 0;
    // assume the traversal is sound until a cell says otherwise
    auto sound = true;
    // go through every index the layout generates
    for (auto it = packing.begin(); it != packing.end(); ++it) {
        // work out where this index lives in memory
        auto offset = packing.offset(*it);
        // if the traversal skipped, doubled back, or otherwise strayed
        if (offset != expected) {
            // say where it went instead of where it was due
            channel << pyre::journal::at() << "  " << *it << " -> " << offset << ", expected "
                    << expected << pyre::journal::newline;
            // and remember that this order is mishandled
            sound = false;
        }
        // line up the offset we want next
        ++expected;
    }
    // a complete sweep must also have accounted for every addressable cell
    return sound && expected == static_cast<canonical_t::difference_type>(packing.cells());
}


// verify that the traversal order agrees with the packing order, for every packing order
int
main(int argc, char * argv[])
{
    // initialize the journal
    pyre::journal::init(argc, argv);
    // attribute whatever gets logged to this test
    pyre::journal::application("canonical_visit_order");
    // make a channel
    pyre::journal::debug_t channel("pyre.grid.canonical");

    // give every axis a different extent, so that a mistaken traversal cannot be masked by the
    // extents happening to line up
    constexpr shape_t shape { 2, 3, 4, 5 };

    // room for the axis labels we will permute
    order_t::storage_type labels {};
    // start from the identity, which packs the leading axis fastest
    for (canonical_t::size_type axis = 0; axis < canonical_t::rank(); ++axis) {
        labels[axis] = axis;
    }

    // every permutation of the axis labels is a legitimate packing order, and each one has to be
    // walked correctly; the two conventional orders are their own inverse, so only sweeping the
    // whole symmetric group catches a traversal that reads the packing order backwards
    do {
        // adopt this permutation as the packing order
        const order_t order { labels };
        // which had better be a genuine permutation, or the layout means nothing
        assert(order.isPermutation());
        // lay out a grid that packs its axes this way
        const canonical_t packing { shape, {}, order };
        // name the order on trial, so that a failure below can be attributed
        channel << pyre::journal::at() << "order: " << order << pyre::journal::newline;
        // and check that walking it agrees with the memory it describes
        assert(visitsInMemoryOrder(packing, channel));
    } while (std::next_permutation(labels.begin(), labels.end()));

    // flush the trace
    channel << pyre::journal::endl;

    // all done
    return 0;
}


// end of file
