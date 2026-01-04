// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// support
#include <array>
#include <cassert>
#include <numeric>
// get the grid
#include <pyre/grid.h>


// type alias
using canonical_t = pyre::grid::canonical_t<3, long>;


// verify that the layout is recorded as requested
int
main(int argc, char * argv[])
{
    // initialize the journal
    pyre::journal::init(argc, argv);
    pyre::journal::application("canonical_offset");
    // make a channel
    auto channel = pyre::journal::debug_t("pyre.grid.canonical");

    // pick a shape
    canonical_t::shape_type shape { 1 << 12, 1 << 12, 1 << 12 };
    // make a canonical packing strategy
    canonical_t packing { shape };

    // show me
    channel
        // shape
        << "shape: " << packing.shape()
        << pyre::journal::newline
        // origin
        << "origin: " << packing.origin()
        << pyre::journal::newline
        // order
        << "order: " << packing.order()
        << pyre::journal::newline
        // strides
        << "strides: " << packing.strides()
        << pyre::journal::newline
        // nudge
        << "nudge: " << packing.nudge()
        << pyre::journal::newline
        // total number of cells
        << "cells: " << packing.cells()
        << pyre::journal::newline
        // flush
        << pyre::journal::endl;

    // verify we understand the default constructor
    assert((packing.shape() == shape));
    assert((packing.order() == canonical_t::order_type::c()));
    assert((packing.origin() == canonical_t::index_type::zero()));
    assert((packing.nudge() == packing[{ 0, 0, 0 }]));

    // make an index
    auto index = canonical_t::index_type().fill((1 << 12) - 1);
    // show me
    channel
        // the index
        << "index: " << index
        << pyre::journal::newline
        // the offset
        << "offset: " << packing.offset(index)
        << pyre::journal::newline
        // inner product
        << "inner product: "
        << std::inner_product(index.begin(), index.end(), packing.strides().begin(), 0UL)
        << pyre::journal::newline
        // flush
        << pyre::journal::endl;
    // check
    assert(
        std::inner_product(index.begin(), index.end(), packing.strides().begin(), 0UL)
        == packing.offset(index));

    // all done
    return 0;
}


// end of file
