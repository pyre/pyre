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


// a finite subset of the integer lattice of dimension {dim}: the points whose coordinates lie
// between a lowest and a highest corner, both included; a catalog of tracks and frames is one
template <std::size_t dim>
class pyre::geometry::Lattice {
    // type aliases
public:
    // me
    using self_type = Lattice<dim>;
    // my coordinates
    using coordinate_type = long;
    // my points
    using rep_type = std::array<coordinate_type, dim>;
    using point_type = Point<self_type>;
    // indices
    using size_type = size_t;

    // metamethods
public:
    // the lattice points between the {lowest} and the {highest} corners
    constexpr Lattice(const rep_type & lowest, const rep_type & highest);

    // the rest
    constexpr Lattice(const Lattice &) = default;
    constexpr Lattice(Lattice &&) = default;
    constexpr Lattice & operator=(const Lattice &) = default;
    constexpr Lattice & operator=(Lattice &&) = default;
    constexpr ~Lattice() = default;

    // equality: lattices with the same corners are the same space
    constexpr auto operator==(const Lattice &) const -> bool = default;

    // interface
public:
    // my dimension
    static constexpr auto dimension() -> size_type;
    // my corners
    constexpr auto lowest() const -> const rep_type &;
    constexpr auto highest() const -> const rep_type &;
    // the number of my points
    constexpr auto cells() const -> size_type;
    // check whether a point belongs to me
    constexpr auto contains(const point_type & p) const -> bool;

    // rendering
public:
    // write a point as its comma separated coordinates
    static auto inject(std::ostream & stream, const rep_type & p) -> void;

    // implementation details - data
private:
    rep_type _lowest;
    rep_type _highest;
};


// get the inline definitions
#include "Lattice.icc"


// end of file
