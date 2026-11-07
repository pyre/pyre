// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// my dependencies
#include "forward.h"
#include "Point.h"


// the cartesian product of two spaces: its points are pairs of points, one from each factor
template <class firstT, class secondT>
class pyre::geometry::Product {
    // type aliases
public:
    // me
    using self_type = Product<firstT, secondT>;
    // my factors
    using first_type = firstT;
    using second_type = secondT;
    // my points
    using rep_type = std::pair<Point<first_type>, Point<second_type>>;
    using point_type = Point<self_type>;
    // indices
    using size_type = size_t;

    // metamethods
public:
    // the product of the two given spaces
    constexpr Product(const first_type & first, const second_type & second);

    // the rest
    constexpr Product(const Product &) = default;
    constexpr Product(Product &&) = default;
    constexpr Product & operator=(const Product &) = default;
    constexpr Product & operator=(Product &&) = default;
    constexpr ~Product() = default;

    // equality: products of the same factors are the same space
    constexpr auto operator==(const Product &) const -> bool = default;

    // interface
public:
    // my dimension is the sum of the dimensions of my factors
    static constexpr auto dimension() -> size_type;
    // my factors
    constexpr auto first() const -> const first_type &;
    constexpr auto second() const -> const second_type &;

    // rendering
public:
    // write a point as its two parts
    static auto inject(std::ostream & stream, const rep_type & p) -> void;

    // implementation details - data
private:
    first_type _first;
    second_type _second;
};


// get the inline definitions
#include "Product.icc"


// end of file
