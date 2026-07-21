// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// support
#include <cassert>
// get the grid
#include <pyre/grid.h>


// the indices under test, of several ranks
using index1_t = pyre::grid::index_t<1>;
using index3_t = pyre::grid::index_t<3>;
using index4_t = pyre::grid::index_t<4>;


// exercise the cartesian product, which joins two indices into one of the combined rank
int
main(int argc, char * argv[])
{
    // initialize the journal
    pyre::journal::init(argc, argv);
    // attribute whatever gets logged to this test
    pyre::journal::application("index_cartesian");
    // make a channel
    pyre::journal::debug_t channel("pyre.grid.index");

    // a one dimensional index
    constexpr index1_t one { 1 };
    // and a three dimensional one
    constexpr index3_t three { 1, 1, 1 };

    // their product lays the first index's axes ahead of the second's
    constexpr auto joined = one * three;
    // show me
    channel << "one: " << one << pyre::journal::newline << "three: " << three
            << pyre::journal::newline << "joined: " << joined << pyre::journal::endl(__HERE__);

    // the rank of the product is the sum of the ranks
    static_assert(decltype(joined)::rank() == 4);
    // and the type is a genuine index of that rank
    static_assert(std::is_same_v<decltype(joined), const index4_t>);

    // the leading axes are the first index, the trailing ones the second
    static_assert(joined == index4_t { 1, 1, 1, 1 });

    // so a product makes a natural shift for widening an index of matching rank
    constexpr index4_t sample { 1, 2, 3, 4 };
    // grown by the joined unit shift
    constexpr index4_t grown = sample + joined;
    // every coordinate advanced by one
    static_assert(grown == index4_t { 2, 3, 4, 5 });

    // all done
    return 0;
}


// end of file
