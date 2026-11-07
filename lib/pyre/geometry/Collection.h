// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// my dependencies
#include "forward.h"


// a finite union of shapes of the same kind; its members may overlap, touch, or lie apart, so a
// collection describes a set that need not be connected
template <class shapeT>
class pyre::geometry::Collection {
    // type aliases
public:
    // me
    using self_type = Collection<shapeT>;
    // my members
    using shape_type = shapeT;
    using shapes_type = std::vector<shape_type>;
    // the envelope of my members, and so mine
    using envelope_type = typename shape_type::envelope_type;
    // indices
    using size_type = size_t;

    // metamethods
public:
    // the empty union
    constexpr Collection() = default;
    // the union of the given {shapes}
    constexpr explicit Collection(shapes_type shapes);
    // the union of the shapes in the list
    constexpr Collection(std::initializer_list<shape_type> shapes);

    // the rest
    constexpr Collection(const Collection &) = default;
    constexpr Collection(Collection &&) = default;
    constexpr Collection & operator=(const Collection &) = default;
    constexpr Collection & operator=(Collection &&) = default;
    constexpr ~Collection() = default;

    // equality: collections with the same members in the same order
    constexpr auto operator==(const Collection &) const -> bool = default;

    // interface
public:
    // the number of my members
    constexpr auto size() const -> size_type;
    // support for ranged for loops
    constexpr auto begin() const;
    constexpr auto end() const;
    // the smallest envelope that holds all my members, for the members whose envelopes have
    // a hull
    constexpr auto envelope() const -> envelope_type;

    // implementation details - data
private:
    shapes_type _shapes;
};


// get the inline definitions
#include "Collection.icc"


// end of file
