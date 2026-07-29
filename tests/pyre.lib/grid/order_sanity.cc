// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// support
#include <cassert>
// get the grid
#include <pyre/grid.h>


// the packing order under test
using order_t = pyre::grid::order_t<4>;


// sanity check
int
main(int argc, char * argv[])
{
    // initialize the journal
    pyre::journal::init(argc, argv);
    // attribute whatever gets logged to this test
    pyre::journal::application("order_sanity");
    // make a channel
    pyre::journal::debug_t channel("pyre.grid.order");

    // verify that the rank is reported correctly through the type
    static_assert(order_t::rank() == 4);

    // make an explicitly initialized ordering
    constexpr order_t shuffle { 0, 1, 2, 3 };
    // show me
    channel << pyre::journal::at() << "an ordering: " << shuffle << pyre::journal::endl;
    // it must be a genuine permutation of the axis labels
    static_assert(shuffle.isPermutation());

    // make a column major ordering
    constexpr order_t fortran = order_t::fortran();
    // show me
    channel << pyre::journal::at() << "fortran: " << fortran << pyre::journal::endl;
    // column major visits the axes in their natural sequence, so it matches {shuffle}
    static_assert(shuffle == fortran);

    // make a row major ordering
    constexpr order_t c = order_t::c();
    // show me
    channel << pyre::journal::at() << "c: " << c << pyre::journal::endl;
    // row major reverses the axis sequence, so it differs from {shuffle}
    static_assert(shuffle != c);
    // and it is a permutation just the same
    static_assert(c.isPermutation());

    // the default ordering is row major
    constexpr order_t dflt {};
    // show me
    channel << pyre::journal::at() << "default: " << dflt << pyre::journal::endl;
    // verify the claim
    static_assert(dflt == c);

    // {c} is the language flavored spelling of row major
    static_assert(order_t::c() == order_t::rowMajor());
    // and {fortran} of column major
    static_assert(order_t::fortran() == order_t::columnMajor());

    // all done
    return 0;
}


// end of file
