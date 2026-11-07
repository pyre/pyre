// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// my dependencies
#include "forward.h"
#include "concepts.h"
#include "Point.h"


// the affine structure of the spaces that have one
namespace pyre::geometry {
    // the vector from {q} to {p}
    template <affine_space_c spaceT>
    constexpr auto operator-(const Point<spaceT> & p, const Point<spaceT> & q) ->
        typename spaceT::vector_type;

    // the point {p} translated by the vector {v}
    template <affine_space_c spaceT>
    constexpr auto operator+(const Point<spaceT> & p, const typename spaceT::vector_type & v)
        -> Point<spaceT>;

    // the point {p} translated by the opposite of the vector {v}
    template <affine_space_c spaceT>
    constexpr auto operator-(const Point<spaceT> & p, const typename spaceT::vector_type & v)
        -> Point<spaceT>;
} // namespace pyre::geometry


// get the inline definitions
#include "algebra.icc"


// end of file
