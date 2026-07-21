// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// support
#include <cassert>
// get the grid
#include <pyre/_grid_.h>


// the shapes under test, of several ranks
using shape1_t = pyre::grid::shape_t<1>;
using shape3_t = pyre::grid::shape_t<3>;
using shape4_t = pyre::grid::shape_t<4>;


// exercise the cartesian product, which joins two shapes into one of the combined rank
int
main(int argc, char * argv[])
{
    // initialize the journal
    pyre::journal::init(argc, argv);
    // attribute whatever gets logged to this test
    pyre::journal::application("shape_cartesian");
    // make a channel
    pyre::journal::debug_t channel("pyre.grid.shape");

    // a one dimensional shape
    constexpr shape1_t one { 1 };
    // and a three dimensional one
    constexpr shape3_t three { 1, 1, 1 };

    // their product lays the first shape's axes ahead of the second's
    constexpr auto joined = one * three;
    // show me
    channel << "one: " << one << pyre::journal::newline << "three: " << three
            << pyre::journal::newline << "joined: " << joined << pyre::journal::endl(__HERE__);

    // the rank of the product is the sum of the ranks
    static_assert(decltype(joined)::rank() == 4);
    // and the type is a genuine shape of that rank
    static_assert(std::is_same_v<decltype(joined), const shape4_t>);
    // its cell count is the product of the two cell counts
    static_assert(joined.cells() == one.cells() * three.cells());

    // so a product makes a natural unit shift for widening a shape of matching rank
    constexpr shape4_t sample { 1, 2, 3, 4 };
    // grown by the joined unit shift
    constexpr shape4_t grown = sample + joined;
    // every extent advanced by one
    static_assert(grown == shape4_t { 2, 3, 4, 5 });

    // all done
    return 0;
}


// end of file
