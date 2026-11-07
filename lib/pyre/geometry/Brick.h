// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// my dependencies
#include "forward.h"


// a logical parallelepiped of dimension {dim}: a container of its 2^dim corners, whose type is a
// template parameter; the space the corners live in may have more dimensions than the brick
template <std::size_t dim, typename nodeT>
class pyre::geometry::Brick {
    // type aliases
public:
    // me
    using self_type = Brick<dim, nodeT>;
    // my corners
    using node_type = nodeT;
    // my parts: 2^dim corners
    using rep_type = std::array<node_type, 1 << dim>;
    // indices
    using size_type = size_t;
    // my bounding box, as its lowest and highest corners
    using box_type = std::pair<typename node_type::rep_type, typename node_type::rep_type>;

    // metamethods
public:
    // build a brick from its corners; copies and moves of bricks are left to the members below
    template <typename... cornerT>
        requires(
            not(sizeof...(cornerT) == 1
                and (std::is_same_v<std::remove_cvref_t<cornerT>, self_type> and ...)))
    inline Brick(cornerT... corner);

    // the rest
    Brick(const Brick &) = default;
    Brick(Brick &&) = default;
    Brick & operator=(const Brick &) = default;
    Brick & operator=(Brick &&) = default;
    ~Brick() = default;

    // interface
public:
    // the dimension of the underlying space
    inline constexpr static auto dimension();
    // the intrinsic dimension of the brick
    inline constexpr static auto intrinsicDimension();
    // the number of points in the brick
    inline constexpr static auto size();

    // check whether the given point is interior
    inline auto interior(const node_type & p) const;

    // compute my characteristic scale
    inline double eigenlen() const;
    // compute my bounding box
    inline auto box() const;
    // enlarge the given box so that it fits me
    inline auto fit(box_type & box) const;

    // indexed access
    inline auto operator[](size_type item) const;

    // support for ranged for loops
    inline auto begin() const;
    inline auto end() const;

    // implementation details
private:
    rep_type _corners;
};


// get the inline definitions
#include "Brick.icc"


// end of file
