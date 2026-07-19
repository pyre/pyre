// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// support
#include "forward.h"


// runtime-rank forward iterator that generates sequences of index vectors
// visiting every point in a box in a prescribed traversal order
//
// this is the counterpart of {IndexIterator<Rank>} for grids whose rank is not known until
// construction time: the parts are {std::vector}s sized by the box being visited rather
// than fixed size {std::array}s, which is what lets the Python bindings iterate over grids
// whose rank is a runtime property
class pyre::grid::DynamicIndexIterator {
    // types
public:
    // basic
    using size_type = size_t;
    using difference_type = std::ptrdiff_t;
    // parts
    using index_type = std::vector<difference_type>;
    using shape_type = std::vector<size_type>;
    using order_type = std::vector<size_type>;
    // iterator traits for STL compatibility
    using value_type = index_type;
    using reference = const index_type &;
    using pointer = const index_type *;
    using iterator_category = std::forward_iterator_tag;

    // metamethods
public:
    // singular iterator; satisfies std::regular
    DynamicIndexIterator() = default;
    // construct from shape, order, and starting position; unit step along each axis
    DynamicIndexIterator(const shape_type &, const order_type &, const index_type &) noexcept;
    // construct with an explicit step along each axis
    DynamicIndexIterator(
        const shape_type &, const order_type &, const index_type &,
        const index_type &) noexcept;

    // default special members
public:
    ~DynamicIndexIterator() = default;
    DynamicIndexIterator(const DynamicIndexIterator &) = default;
    DynamicIndexIterator(DynamicIndexIterator &&) = default;
    auto operator=(const DynamicIndexIterator &) -> DynamicIndexIterator & = default;
    auto operator=(DynamicIndexIterator &&) -> DynamicIndexIterator & = default;

    // iterator protocol
public:
    // the index I am currently parked on
    [[nodiscard]] auto operator*() const noexcept -> reference;
    // step to the next index in traversal order
    auto operator++() noexcept -> DynamicIndexIterator &;
    // step forward, but report the index I was on before the step
    auto operator++(int) noexcept -> DynamicIndexIterator;

    // implementation details
private:
    // where I am in the index box
    index_type _current {};
    // the extent of the box along each axis
    shape_type _shape {};
    // the packing order that dictates the traversal sequence
    order_type _order {};
    // the corner of the box, which is both my starting point and the value each axis
    // resets to when it overflows
    index_type _origin {};
    // how far to move along each axis on every visit
    index_type _step {};
};


// equality: two iterators are equal when they point to the same index
namespace pyre::grid {
    inline auto operator==(
        const DynamicIndexIterator &, const DynamicIndexIterator &) noexcept -> bool;
}


// get the inline implementations
#include "DynamicIndexIterator.icc"


// end of file
