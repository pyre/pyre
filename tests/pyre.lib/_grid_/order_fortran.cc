// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// support
#include <cassert>
// get the grid
#include <pyre/_grid_.h>


// the packing order under test
using order_t = pyre::grid::order_t<4>;


// exercise the column major factory
int
main(int argc, char * argv[])
{
    // initialize the journal
    pyre::journal::init(argc, argv);
    // attribute whatever gets logged to this test
    pyre::journal::application("order_fortran");
    // make a channel
    pyre::journal::debug_t channel("pyre.grid.order");

    // the fortran convention packs the leading axis fastest
    constexpr order_t columnMajor = order_t::fortran();
    // show me
    channel << "column major: " << columnMajor << pyre::journal::endl(__HERE__);

    // so it names the axes in their natural sequence
    static_assert(columnMajor[0] == 0);
    static_assert(columnMajor[1] == 1);
    static_assert(columnMajor[2] == 2);
    static_assert(columnMajor[3] == 3);

    // which is a genuine permutation of the axis labels
    static_assert(columnMajor.isPermutation());

    // all done
    return 0;
}


// end of file
