// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2025 all rights reserved

// code guard
#pragma once


// get the external declaration
#include "externals.h"
// grab the concepts
#include "concepts.h"

// set up the namespace
namespace pyre::grid {
    // packing order
    template <size_t Rank>
    class Order;

    // shape
    template <size_t Rank>
    class Shape;

    // the grid
    template <concepts::PackingStrategy P, concepts::StorageStrategy S>
    class Grid;
} // namespace pyre::grid


// end of file
