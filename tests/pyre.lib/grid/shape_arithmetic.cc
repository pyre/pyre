// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// support
#include <cassert>
// get the grid
#include <pyre/grid.h>


// the shape under test
using shape_t = pyre::grid::shape_t<3>;


// exercise the component-wise arithmetic
int
main(int argc, char * argv[])
{
    // initialize the journal
    pyre::journal::init(argc, argv);
    // attribute whatever gets logged to this test
    pyre::journal::application("shape_arithmetic");
    // make a channel
    pyre::journal::debug_t channel("pyre.grid.shape");

    // extents are spelled with ordinary integer literals, without decoration
    constexpr shape_t big { 4, 5, 6 };
    // as is any other shape
    constexpr shape_t small { 1, 2, 3 };

    // growing a shape adds the extents axis by axis
    constexpr shape_t sum = big + small;
    // show me
    channel << "sum: " << sum << pyre::journal::endl;
    // verify
    static_assert(sum == shape_t { 5, 7, 9 });

    // and shrinking subtracts them
    constexpr shape_t difference = big - small;
    // show me
    channel << "difference: " << difference << pyre::journal::endl;
    // verify
    static_assert(difference == shape_t { 3, 3, 3 });

    // a difference that runs past zero reports a negative extent rather than wrapping to an
    // enormous positive one; the result is not a meaningful shape, but it is a value the caller
    // can recognize as wrong
    constexpr shape_t underflow = small - big;
    // show me
    channel << "underflow: " << underflow << pyre::journal::endl;
    // every axis went below zero, and says so
    static_assert(underflow[0] == -3);
    static_assert(underflow[1] == -3);
    static_assert(underflow[2] == -3);
    // which is a thing a caller can test for
    static_assert(underflow.min() < 0);

    // all done
    return 0;
}


// end of file
