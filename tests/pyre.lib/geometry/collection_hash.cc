// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// check that equal unions hash alike, and that the order of the members shapes the hash, since
// unions compare their members in order


// portability
#include <portinfo>
// STL
#include <cassert>
// support
#include <pyre/geometry.h>


// type aliases
using line_t = pyre::geometry::euclidean_t<1>;
using point_t = pyre::geometry::point_t<line_t>;
using interval_t = pyre::geometry::interval_t<line_t>;
using union_t = pyre::geometry::collection_t<interval_t>;


// driver
int
main()
{
    // two pieces
    auto first = interval_t(point_t(0.0), point_t(1.0));
    auto second = interval_t(point_t(2.0), point_t(3.0));

    // their union
    auto pieces = union_t { first, second };
    // hashes like another made the same way
    assert(pieces.hash() == (union_t { first, second }).hash());
    // the union with its members in the other order
    auto swapped = union_t { second, first };
    // is a different union
    assert(pieces != swapped);
    // with a different hash
    assert(pieces.hash() != swapped.hash());
    // and the empty union hashes like itself
    assert(union_t().hash() == union_t().hash());

    // all done
    return 0;
}


// end of file
