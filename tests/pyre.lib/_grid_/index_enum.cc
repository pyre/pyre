// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// support
#include <cassert>
// get the grid
#include <pyre/_grid_.h>


// the index under test, one axis for polarization and one for color
using index_t = pyre::grid::index_t<2>;


// named coordinates along the polarization axis; a class of named constants stands in for an
// {enum}, which does not convert cleanly to the index cell type
class pol {
public:
    // the four polarization channels
    static constexpr index_t::value_type hh = 0;
    static constexpr index_t::value_type hv = 1;
    static constexpr index_t::value_type vh = 2;
    static constexpr index_t::value_type vv = 3;
};

// named coordinates along the color axis
class color {
public:
    // the three color channels
    static constexpr index_t::value_type red = 0;
    static constexpr index_t::value_type green = 1;
    static constexpr index_t::value_type blue = 2;
};


// verify that named constants can be used to build and read an index
int
main(int argc, char * argv[])
{
    // initialize the journal
    pyre::journal::init(argc, argv);
    // attribute whatever gets logged to this test
    pyre::journal::application("index_enum");
    // make a channel
    pyre::journal::debug_t channel("pyre.grid.index");

    // an index built from the named channels rather than bare numbers
    constexpr index_t idx { pol::hv, color::blue };
    // show me
    channel << "index: " << idx << pyre::journal::endl(__HERE__);

    // the coordinates read back as the named values
    static_assert(idx[0] == pol::hv);
    static_assert(idx[1] == color::blue);

    // all done
    return 0;
}


// end of file
