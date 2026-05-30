// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// support
#include "forward.h"


// runtime-rank forward iterator that generates sequences of index vectors
// visiting every point in a box in a prescribed traversal order
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
    [[nodiscard]] auto operator*() const noexcept -> reference;
    auto operator++() noexcept -> DynamicIndexIterator &;
    auto operator++(int) noexcept -> DynamicIndexIterator;

    // implementation details
private:
    index_type _current {};
    shape_type _shape {};
    order_type _order {};
    index_type _origin {};
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
