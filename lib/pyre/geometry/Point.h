// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// my dependencies
#include "forward.h"


// an element of a space; the space decides how its points are stored, so a point carries no
// instance of its space, and the measures that depend on the parameters of the space, such as
// the radius of a sphere, are computed by the space
template <class spaceT>
class pyre::geometry::Point {
    // type aliases
public:
    // me
    using self_type = Point<spaceT>;
    // my space
    using space_type = spaceT;
    // my storage
    using rep_type = typename space_type::rep_type;
    // indices
    using size_type = size_t;

    // metamethods
public:
    // build a point from the parts of its storage; copies and moves of points are left to the
    // members below
    template <typename... argT>
        requires(
            not(sizeof...(argT) == 1
                and (std::is_same_v<std::remove_cvref_t<argT>, self_type> and ...)))
    constexpr explicit Point(argT &&... args);

    // the rest
    constexpr Point(const Point &) = default;
    constexpr Point(Point &&) = default;
    constexpr Point & operator=(const Point &) = default;
    constexpr Point & operator=(Point &&) = default;
    constexpr ~Point() = default;

    // equality
    constexpr auto operator==(const Point &) const -> bool = default;

    // interface
public:
    // the dimension of the underlying space
    static constexpr auto dimension() -> size_type;
    // access to my storage
    constexpr auto data() const -> const rep_type &;

    // indexed access, for the spaces whose points are arrays
    constexpr auto operator[](size_type item) const
        requires requires(const rep_type & rep) { rep[0]; };

    // support for ranged for loops, for the spaces whose points are arrays
    constexpr auto begin() const
        requires requires(const rep_type & rep) { rep.cbegin(); };
    constexpr auto end() const
        requires requires(const rep_type & rep) { rep.cend(); };

    // implementation details - data
private:
    rep_type _rep;
};


// get the inline definitions
#include "Point.icc"


// end of file
