// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// support
#include "forward.h"


// iterator that generates the sequence of indices that visit every point in a box
// in a traversal order determined by an {Order}
template <std::size_t Rank>
class pyre::grid::IndexIterator {
    // types
public:
    // myself
    using self_type = IndexIterator<Rank>;
    // my parts
    using index_type = Index<Rank>;
    using shape_type = Shape<Rank>;
    using order_type = Order<Rank>;
    // iterator traits for STL compatibility
    // what a dereference yields: a point in index space
    using value_type = index_type;
    // the current index is owned by me, so clients only ever get to look at it
    using reference = const index_type &;
    using pointer = const index_type *;
    using difference_type = std::ptrdiff_t;
    // i can only move forward, and only one index at a time
    using iterator_category = std::forward_iterator_tag;

    // metamethods
public:
    // singular iterator; satisfies the std::regular requirement on forward iterators
    constexpr IndexIterator() noexcept = default;
    // construct from a shape, a traversal order, and a starting index; unit step
    constexpr IndexIterator(
        const shape_type &, const order_type &, const index_type &) noexcept;
    // construct with an explicit step along each axis
    constexpr IndexIterator(
        const shape_type &, const order_type &, const index_type &,
        const index_type &) noexcept;

    // default metamethods
public:
    ~IndexIterator() = default;
    IndexIterator(const IndexIterator &) noexcept = default;
    IndexIterator(IndexIterator &&) noexcept = default;
    auto operator=(const IndexIterator &) noexcept -> self_type & = default;
    auto operator=(IndexIterator &&) noexcept -> self_type & = default;

    // iterator protocol
public:
    // hand out the index i am parked on
    [[nodiscard]] constexpr auto operator*() const noexcept -> reference;
    // move on to the next index in the traversal
    constexpr auto operator++() noexcept -> self_type &;
    // same, but report the index i was parked on before i moved
    constexpr auto operator++(int) noexcept -> self_type;

    // implementation details
private:
    // where i am parked right now
    index_type _current {};
    // the extent of the box i am sweeping
    shape_type _shape {};
    // the axis ranking that decides which axis i advance first
    order_type _order {};
    // the corner of the box that anchors the sweep
    index_type _origin {};
    // how far to move along each axis on every advance
    index_type _step {};
};


// get the inline implementations
#include "IndexIterator.icc"


// end of file
